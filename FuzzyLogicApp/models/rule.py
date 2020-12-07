from decimal import Decimal;

from models.rule_condition import RuleCondition;
from enums.logical_connective_enum import LogicalConnectiveEnum;

class Rule:
    def __str__(self):
        value = "Rule: " + self.Name + "\n"

        for condition in self.Conditions:
            value += str(condition) + "\n";
            continue;

        value += "\t=>" + str(self.Result);

        return value;

    # a bit too lengthy for a constructor
    def __init__(self, ruleText):
        self.Name = str();
        self.Conditions = list();
        self.Result = None; # Condition type

        ruleText = ruleText.lower()

        # get rule name
        ruleName = ruleText\
            .split(":")[0]\
            .strip()

        # remove parsed data
        ruleText = ruleText\
            .split(":")[1]\
            .strip()

        # first condition
        variableIsNegated = False;
        variableOpeningBrackets = 0;
        variableClosingBrackets = 0;

        variableName = ruleText\
            .split("if")[1]\
            .split("is")[0]\
            .strip()

        variableValue = ruleText\
            .split("is")[1]\
            .strip()\
            .split(" ")[0]\
            .strip()

        if "not" in variableValue:
            variableValue =  ruleText\
                .split("is")[1]\
                .strip()\
                .split(" ")[1]\
                .strip()
            variableIsNegated = True;

        # remove parsed data
        ruleText = ruleText\
            .split(variableValue)[1]\
            .strip()

        # set the result
        positiveRuleResult = ruleText\
            .split(" then ")[1]\
            .strip()

        resultVariableIsNegated = False;
        resultOpeningBrackets = 0;
        resultClosingBrackets = 0;

        resultVariableName = positiveRuleResult\
            .split(" is ")[0]\
            .strip()

        resultVariableValue = positiveRuleResult\
            .split(" is ")[1]\
            .strip()

        if "not" in resultVariableValue:
            resultVariableValue = ositiveRuleResult\
                .split(" is ")[2]\
                .strip()
            resultVariableIsNegated = True;

        # removing parsed data
        ruleText = ruleText\
            .split(" then ")[0]\
            .strip()

        # chained and/or connectives, this is just a hacky way of making sure
        # we split all connectives.
        # this however might break on unknown connectives.
        chainedConditions = ruleText\
            .replace("and ", "#and# ")\
            .replace("or ", "#or# ")\
            .split("#");

        # TODO: get rid of empty entries, couldn't figure out a neater way to do it. Definitely hacky
        if "" in chainedConditions:
            chainedConditions.remove("");

        # actual Initialization
        firstCondition = RuleCondition(\
            LogicalConnectiveEnum._None,\
            variableIsNegated,\
            variableOpeningBrackets,\
            variableClosingBrackets,\
            variableName,\
            variableValue)

        self.Result = RuleCondition(\
           LogicalConnectiveEnum._None,\
           resultVariableIsNegated,\
           resultOpeningBrackets,\
           resultClosingBrackets,\
           resultVariableName,\
           resultVariableValue)

        self.Conditions\
            .append(firstCondition)

        # add subsequent conditions
        for i in range(0, len(chainedConditions), 2):
            connective = chainedConditions[i];
            variable = chainedConditions[i+1];

            chainedVariableConnectiveText = connective.strip();

            chainedVariableConnectiveEnum = \
                LogicalConnectiveEnum.And if chainedVariableConnectiveText == str(LogicalConnectiveEnum.And) \
                else LogicalConnectiveEnum.Or if chainedVariableConnectiveText == str(LogicalConnectiveEnum.Or) \
                else LogicalConnectiveEnum._None

            if (chainedVariableConnectiveEnum == LogicalConnectiveEnum._None):
                # something not right, cannot have subsequent conditions with
                # None or unknown connectives
                print("Incorrect Logical Connective used for subsequent condition - ", chainedVariableConnectiveText)
                continue

            chainedVariableIsNegated = False;
            chainedVariableOpeningBrackets = 0;
            chainedVariableClosingBrackets = 0;

            chainedVariableName = variable\
                .split(" is ")[0]\
                .split(" ")[1]\
                .strip()

            chainedVariableValue = variable\
                .split(" is ")[1]\
                .strip()\
                .split(" ")[0]\
                .strip()

            if "not" in chainedVariableValue:
                chainedVariableValue = variable\
                    .split(" is ")[1]\
                    .strip()\
                    .split(" ")[1]\
                    .strip()
                chainedVariableIsNegated = True;

            self.Conditions.append(RuleCondition(\
                chainedVariableConnectiveEnum,\
                chainedVariableIsNegated,\
                chainedVariableOpeningBrackets,\
                chainedVariableClosingBrackets,\
                chainedVariableName,\
                chainedVariableValue))

        self.Name = ruleName
        return;