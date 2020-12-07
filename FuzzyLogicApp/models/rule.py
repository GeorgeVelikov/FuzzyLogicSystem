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

        self.Name = ruleName

        # remove parsed data
        ruleText = ruleText\
            .split("if ")[1]\
            .strip()

        firstCondition = self.GetCondition(ruleText);

        self.Conditions\
            .append(firstCondition);

        # remove parsed data
        ruleText = ruleText\
            .split(firstCondition.VariableValue)[1][firstCondition.ClosingBracketsCount:]\
            .strip()

        # text to get result from
        resultText = ruleText\
            .split(" then ")[1]\
            .strip()

        resultCondition = self.GetCondition(resultText);
        self.Result = resultCondition;

        # remove parsed data
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

            chainedCondition = self.GetCondition(variable);
            chainedCondition.LogicalConnective = chainedVariableConnectiveEnum;

            self.Conditions.append(chainedCondition);
        return;

    def GetCondition(self, ruleText):
        variableName = str();
        variableValue = str();
        variableIsNegated = False;
        variableOpeningBrackets = 0;
        variableClosingBrackets = 0;

        variableName = ruleText\
            .split("is")[0]\
            .strip()

        if "(" in variableName:
            variableOpeningBrackets = variableName.count("(");
            variableName = variableName.replace("(", str());

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

        if ")" in variableValue:
            variableClosingBrackets = variableValue.count(")");
            variableValue = variableValue.replace(")", str());

        return RuleCondition(\
            LogicalConnectiveEnum._None,\
            variableIsNegated,\
            variableOpeningBrackets,\
            variableClosingBrackets,\
            variableName,\
            variableValue);