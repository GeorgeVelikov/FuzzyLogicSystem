# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆
# 🦆     Georgi Velikov     🦆
# 🦆        51660024        🦆
# 🦆 University Of Aberdeen 🦆
# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆

from enum import Enum

class LogicalConnectiveEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    If = 1;
    And = 2;
    Or = 3;
    Then = 4;

    def __str__(self):
        if self.value == self._None.value:
            return str();
        elif self.value == self.If.value:
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
        if self.value == self.If.value:
            return str();
        elif self.value == self.And.value:
            return "&";
        elif self.value == self.Or.value:
            return "|";
        elif self.value == self.Then.value:
            return "=>";

    def Values():
        return [\
            LogicalConnectiveEnum.If,\
            LogicalConnectiveEnum.And,\
            LogicalConnectiveEnum.Or,\
            LogicalConnectiveEnum.Then];
