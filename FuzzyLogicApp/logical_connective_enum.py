from enum import Enum

class LogicalConnectiveEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    And = 1;
    Or = 2;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.And.value:
            return "and";
        elif self.value == self.Or.value:
            return "or";
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

    def Values(self):
        return [self.And,\
            self.Or];
