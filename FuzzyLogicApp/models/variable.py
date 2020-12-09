class Variable:
    def __str__(self):
        return "\t" + self.Name + " defined as " + str(self.Tuple) + " where (A, B, Alpha, Beta)";

    def __init__(self, name, fuzzyTuple):
        self.Name = str();
        self.Tuple = tuple();

        self.Name = name;
        self.Tuple = fuzzyTuple;

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
        return [self.MinValue, self.A, self.B, self.MaxValue];

    @property
    def MinValue(self):
        return self.A - self.Alpha;

    @property
    def MaxValue(self):
        return self.B + self.Beta;

    def RaiseExceptionIfInvalid(self):
        isValid = True;

        if len(list(self.Tuple)) != 4:
            raise Exception("Cannot have variable value tuples with less or more than 4 elements.");
            isValid = False;

        if self.B < self.A:
            raise Exception("B cannot be smaller than A in the tuple " + str(self.Tuple) +\
                ". Where the the tuple is [A, B, Alpha, Beta].");
            isValid = False;

        if self.A < self.MinValue:
            raise Exception("A cannot be smaller than (A - Alpha) in the tuple " + str(self.Tuple) +\
                ". Where the the tuple is [A, B, Alpha, Beta].");
            isValid = False;

        if self.MaxValue < self.B:
            raise Exception("B cannot be smaller than (B + Beta) in the tuple " + str(self.Tuple) +\
                ". Where the the tuple is [A, B, Alpha, Beta].");
            isValid = False;

        return isValid;