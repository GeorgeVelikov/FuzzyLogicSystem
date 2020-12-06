from decimal import Decimal
from logical_connective_enum import LogicalConnectiveEnum

class RuleCondition:
    def __str__(self):
        # probably better to use enum.name instead of literal strings
        connective = \
            "\t" if self.LogicalConnective == LogicalConnectiveEnum._None\
            else "\tand " if self.LogicalConnective == LogicalConnectiveEnum.And\
            else "\tor " if self.LogicalConnective== LogicalConnectiveEnum.Or\
            else "\tUNKNOWN ";

        value = connective + self.VariableName + " is " + self.VariableValue;

        return value;

    def __init__(self, logicalConnective, variableName, variableValue):
        self.LogicalConnective = LogicalConnectiveEnum._None;
        self.VariableName = str();
        # this is the variable value name, a bit confusing
        self.VariableValue = str();

        self.LogicalConnective = logicalConnective;
        self.VariableName = variableName;
        self.VariableValue = variableValue;
        return

    @property
    def GetLogicalConnectiveOperand(self):
        if (self.LogicalConnective == LogicalConnectiveEnum._None):
            return str();
        elif (self.LogicalConnective == LogicalConnectiveEnum.And):
            return "&";
        elif (self.LogicalConnective == LogicalConnectiveEnum.Or):
            return "|";
        else:
            raise Exception("Incorrect logical connective.");

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
        self.Name = ""
        self.Conditions = []
        self.Result = None

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
        variableName = ruleText\
            .split("if")[1]\
            .split("is")[0]\
            .strip()

        variableValue = ruleText\
            .split("is")[1]\
            .strip()\
            .split(" ")[0]\
            .strip()

        # remove parsed data
        ruleText = ruleText\
            .split(variableValue)[1]\
            .strip()

        # set the result
        positiveRuleResult = ruleText\
            .split(" then ")[1]\
            .strip()

        resultVariableName = positiveRuleResult\
            .split(" is ")[0]\
            .strip()

        resultVariableValue = positiveRuleResult\
            .split(" is ")[1]\
            .strip()

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
            variableName,\
            variableValue)

        self.Result = RuleCondition(\
           LogicalConnectiveEnum._None,\
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
                LogicalConnectiveEnum.And if chainedVariableConnectiveText == "and" \
                else LogicalConnectiveEnum.Or if chainedVariableConnectiveText == "or" \
                else LogicalConnectiveEnum._None

            if (chainedVariableConnectiveEnum == LogicalConnectiveEnum._None):
                # something not right, cannot have subsequent conditions with
                # None or unknown connectives
                print("Incorrect Logical Connective used for subsequent condition - ", chainedVariableConnectiveText)
                continue

            chainedVariableName = variable\
                .split(" is ")[0]\
                .split(" ")[1]\
                .strip()

            chainedVariableValue = variable\
                .split(" is ")[1]\
                .strip()\
                .split(" ")[0]\
                .strip()

            self.Conditions.append(RuleCondition(\
               chainedVariableConnectiveEnum,\
               chainedVariableName,\
               chainedVariableValue))

        self.Name = ruleName
        return;