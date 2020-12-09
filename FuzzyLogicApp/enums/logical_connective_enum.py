from enum import Enum

class LogicalConnectiveEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    And = 1;
    Or = 2;
    Then = 3;

    def __str__(self):
        if self.value == self._None.value:
            return "if";
        elif self.value == self.And.value:
            return "and";
        elif self.value == self.Or.value:
            return "or";
        elif self.value == self.Then.value:
            return "then";
        else:
            raise Exception("Invalid Logical Connective used.");

    @property
    def Operand(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.And.value:
            return "&";
        elif self.value == self.Or.value:
            return "|";
        elif self.value == self.Then.value:
            return "=>";

    def Values():
        return [LogicalConnectiveEnum.And,\
            LogicalConnectiveEnum.Or,\
            LogicalConnectiveEnum.Then];
