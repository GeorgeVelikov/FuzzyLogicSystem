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
       return;
