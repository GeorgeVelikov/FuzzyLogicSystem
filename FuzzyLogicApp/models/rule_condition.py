from enums.logical_connective_enum import LogicalConnectiveEnum;

class RuleCondition:
    def __str__(self):
        # probably better to use enum.name instead of literal strings
        value = "\t" + str(self.LogicalConnective) + " " +\
           self.VariableName + " is " + ("not " if self.IsNegated else str()) + self.VariableValue;

        return value;

    def __init__(self, logicalConnective, isNegated, variableName, variableValue):
        self.LogicalConnective = LogicalConnectiveEnum._None;
        self.IsNegated = False;
        self.VariableName = str();
        # this is the variable value name, a bit confusing
        self.VariableValue = str();

        self.LogicalConnective = logicalConnective;
        self.IsNegated = isNegated; #if NOT variable name is variableValue
        self.VariableName = variableName;
        self.VariableValue = variableValue;
        return;

    @property
    def BooleanOperand(self):
        # Idk what to call this, it's effectively a +/- for a boolean value, or in this case a fuzzy set
         return "~" if self.IsNegated else str();