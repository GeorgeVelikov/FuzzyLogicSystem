# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆
# 🦆     Georgi Velikov     🦆
# 🦆        51660024        🦆
# 🦆 University Of Aberdeen 🦆
# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆

from enums.logical_connective_enum import LogicalConnectiveEnum;

class Term:
    def __str__(self):
        value = "\t" +\
            str(self.LogicalConnective) + " " +\
            self.OpeningParentheses + self.VariableName + " is " +\
            ("not " if self.IsNegated else str()) + self.VariableValue + self.ClosingParentheses;

        return value;

    def __init__(self,\
        logicalConnective,\
        isNegated,\
        openingParenthesesCount,\
        closingParenthesesCount,\
        variableName,\
        variableValue):

        self.LogicalConnective = LogicalConnectiveEnum._None;
        self.IsNegated = bool();
        self.OpeningParenthesesCount = int();
        self.ClosingParenthesesCount = int();
        self.VariableName = str();
        self.VariableValue = str();

        self.LogicalConnective = logicalConnective;

        # if variableName is NOT variableValue
        self.IsNegated = isNegated;

        # this is a bit of a hack, this should be the foundation of a new class
        # but for the sake of the first-pass parentheses support, this will work.
        self.OpeningParenthesesCount = openingParenthesesCount;
        self.ClosingParenthesesCount = closingParenthesesCount;

        self.VariableName = variableName;
        self.VariableValue = variableValue;

        return;

    @property
    def BooleanOperand(self):
        # Idk what to call this, BooleanOperands seems to make sense to me 🤷
         return "~" if self.IsNegated else str();

    @property
    def OpeningParentheses(self):
        return self.OpeningParenthesesCount * "(";

    @property
    def ClosingParentheses(self):
        return self.ClosingParenthesesCount * ")";

    def RaiseExceptionIfInvalid(self):
        # add necessary data checks here
        return True;