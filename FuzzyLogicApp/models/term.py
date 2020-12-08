from enums.logical_connective_enum import LogicalConnectiveEnum;

class Term:
    def __str__(self):
        value = "\t" +\
            str(self.LogicalConnective) + " " +\
            self.OpeningBrackets + self.VariableName + " is " +\
            ("not " if self.IsNegated else str()) + self.VariableValue + self.ClosingBrackets;

        return value;

    def __init__(self,\
        logicalConnective,\
        isNegated,\
        openingBracketsCount,\
        closingBracketsCount,\
        variableName,\
        variableValue):

        self.LogicalConnective = LogicalConnectiveEnum._None;
        self.IsNegated = bool();
        self.OpeningBracketsCount = int();
        self.ClosingBracketsCount = int();
        self.VariableName = str();
        self.VariableValue = str();

        self.LogicalConnective = logicalConnective;

        # if variableName is NOT variableValue
        self.IsNegated = isNegated;

        # this is a bit of a hack, this should be the foundation of a new class
        # but for the sake of the first-pass brackets support, this will work.
        self.OpeningBracketsCount = openingBracketsCount;
        self.ClosingBracketsCount = closingBracketsCount;

        self.VariableName = variableName;
        self.VariableValue = variableValue;

        return;

    @property
    def BooleanOperand(self):
        # Idk what to call this, BooleanOperands seems to make sense to me 🤷
         return "~" if self.IsNegated else str();

    @property
    def OpeningBrackets(self):
        return self.OpeningBracketsCount * "(";

    @property
    def ClosingBrackets(self):
        return self.ClosingBracketsCount * ")";