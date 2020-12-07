from logical_connective_enum import LogicalConnectiveEnum;

class RuleCondition:
    def __str__(self):
        # probably better to use enum.name instead of literal strings
        value = "\t" + str(self.LogicalConnective) + " " +\
           self.VariableName + " is " + self.VariableValue;

        return value;

    def __init__(self, logicalConnective, variableName, variableValue):
        self.LogicalConnective = LogicalConnectiveEnum._None;
        self.VariableName = str();
        # this is the variable value name, a bit confusing
        self.VariableValue = str();

        self.LogicalConnective = logicalConnective;
        self.VariableName = variableName;
        self.VariableValue = variableValue;
        return;