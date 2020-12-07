from decimal import Decimal

class Measurement:
    def __str__(self):
        return "\t" + self.Name + " = " + str(self.Value);

    def __init__(self, measurementText):
        self.Name = str();
        self.Value = Decimal();

        name = measurementText\
            .split("=")[0]\
            .strip();

        value = measurementText\
            .split("=")[1]\
            .strip()\
            .split(" ")[0]\
            .strip();

        self.Name = name;
        self.Value = eval(value);

        self.RaiseExceptionIfInvalid();

        return;

    def RaiseExceptionIfInvalid(self):
       return;
