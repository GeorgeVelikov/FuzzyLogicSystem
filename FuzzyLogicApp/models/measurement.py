# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆
# 🦆     Georgi Velikov     🦆
# 🦆        51660024        🦆
# 🦆 University Of Aberdeen 🦆
# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆

from decimal import Decimal

class Measurement:
    def __str__(self):
        return "\t" + self.Name + " = " + str(self.Value);

    def __init__(self, name, value):
        self.Name = str();
        self.Value = Decimal();

        self.Name = name;
        self.Value = value;

        self.RaiseExceptionIfInvalid();

        return;

    def RaiseExceptionIfInvalid(self):
        # add necessary data checks here
        return True;
