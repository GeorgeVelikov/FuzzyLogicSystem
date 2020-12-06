class VariableValue:
    def __str__(self):
        return "\t" + self.Name + " defined in " + str(self.Tuple);

    def __init__(self, variableValueText):
        self.Name = "";
        self.Tuple = [];

        variableName = variableValueText\
            .split(" ")[0]\
            .strip();

        # TODO: what format are we getting?
        variableTupleValue = variableValueText\
            .split(" ", 1)[-1]\
            .replace("[", "")\
            .replace("]", "")\
            .replace("<", "")\
            .replace(">", "")\
            .strip();

        if "," not in variableTupleValue:
            variableTupleValue = variableTupleValue\
                .replace(" ", ",");

        self.Name = variableName;
        self.Tuple = eval(variableTupleValue);

        self.RaiseExceptionIfInvalid();

        return;

    @property
    def A(self):
        return self.Tuple[0];

    @property
    def B(self):
        return self.Tuple[1];

    @property
    def Alpha(self):
        return self.Tuple[2];

    @property
    def Beta(self):
        return self.Tuple[3];

    @property
    def TrapezoidalInput(self):
        return [self.A - self.Alpha, self.A, self.B, self.B + self.Beta];

    @property
    def MinValue(self):
        return self.A - self.Alpha;

    @property
    def MaxValue(self):
        return self.B + self.Beta;

    def RaiseExceptionIfInvalid(self):
        if len(list(self.Tuple)) != 4:
            raise Exception("Cannot have variable value tuples with less or more than 4 elements.");

        if self.B < self.A:
            raise Exception("B cannot be smaller than A in the tuple " + str(self.Tuple) +\
                ". Where the the tuple is [A, B, Alpha, Beta].");