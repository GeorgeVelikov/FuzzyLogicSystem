class VariableMeasurement:

    def __str__(self):
        return "\t" + self.Name + " = " + str(self.Value);

    def __init__(self, variableMeasurementText):
        self.Name = "";
        self.Value = 0;

        measurementName = variableMeasurementText\
            .split("=")[0]\
            .strip();

        measurementValueText = variableMeasurementText\
            .split("=")[1]\
            .strip()\
            .split(" ")[0]\
            .strip();

        self.Name = measurementName;
        self.Value = eval(measurementValueText);

        self.RaiseExceptionIfInvalid();

        return;

    def RaiseExceptionIfInvalid(self):
       return;
