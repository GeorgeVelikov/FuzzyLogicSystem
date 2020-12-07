from enums.logical_connective_enum import LogicalConnectiveEnum;

class RuleCondition:
    def __str__(self):
        # probably better to use enum.name instead of literal strings
        value = "\t" + str(self.LogicalConnective) + " " +\
           self.VariableName + " is " + ("not " if self.IsNegated else str()) + self.VariableValue;

        return value;

    def __init__(self,\
        logicalConnective,\
        isNegated,\
        openingBracketsCount,\
        closingBracketsCount,\
        variableName,\
        variableValue):

        self.LogicalConnective = LogicalConnectiveEnum._None;
        self.IsNegated = False;
        self.OpeningBracketsCount = int();
        self.ClosingBracketsCount = int();
        self.VariableName = str();
        self.VariableValue = str();

        self.LogicalConnective = logicalConnective;

        #if variable name is NOT variableValue
        self.IsNegated = isNegated;

        # this is a bit of a hack, this should be the foundation of a new class - Term
        # but for the sake of the first-pass brackets support, this will work.
        self.OpeningBracketsCount = openingBracketsCount;
        self.ClosingBracketsCount = closingBracketsCount;

        self.VariableName = variableName;
        self.VariableValue = variableValue;
        return;

    @property
    def BooleanOperand(self):
        # Idk what to call this, it's effectively a +/- for a boolean value, or in this case a fuzzy set
         return "~" if self.IsNegated else str();

    @property
    def OpeningBrackets(self):
        return self.OpeningBracketsCount * "(";

    @property
    def ClosingBrackets(self):
        return self.ClosingBracketsCount * ")";