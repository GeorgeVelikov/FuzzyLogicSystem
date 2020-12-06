from enum import Enum

class DefuzzifyingMethodEnum(Enum):
    _None = 0;
    CentroidOfArea = 1;
    BisectorOfArea = 2;
    MeanOfMaximum = 3;
    SmallestOfMaximum = 4;
    LargestOfMaximum = 5;

    def __str__(self):
        if self.value == self.CentroidOfArea.value:
            return "centroid";
        elif self.value == self.BisectorOfArea.value:
            return "bisector";
        elif self.value == self.MeanOfMaximum.value:
            return "mom";
        elif self.value == self.SmallestOfMaximum.value:
            return "som";
        elif self.value == self.LargestOfMaximum.value:
            return "lom";
        else:
            raise Exception("Unknown Defuzzifying Method used");

    def Values(self):
        return [self.CentroidOfArea,\
            self.BisectorOfArea,\
            self.MeanOfMaximum,\
            self.SmallestOfMaximum,\
            self.LargestOfMaximum];
