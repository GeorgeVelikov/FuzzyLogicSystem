from enum import Enum

class LogicalConnectiveEnum(Enum):
    # Can't escape keywords in Python :(
    _None = 0;
    And = 1;
    Or = 2;
