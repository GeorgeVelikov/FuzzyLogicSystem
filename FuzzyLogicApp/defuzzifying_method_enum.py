from enum import Enum

class DefuzzifyingMethodEnum(Enum):
    _None = 0;
    CentroidOfArea = 1;
    BisectorOfArea = 2;
    MeanOfMaximum = 3;
    SmallestOfMaximum = 4;
    LargestOfMaximum = 5;

    def __str__(self):
        # those are the names scikit fuzzy uses to refer to the defuzz methods
        # this is simply a quality of live touches. Figured there's no need to handle _None
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

    def Values():
        return [DefuzzifyingMethodEnum.CentroidOfArea,\
            DefuzzifyingMethodEnum.BisectorOfArea,\
            DefuzzifyingMethodEnum.MeanOfMaximum,\
            DefuzzifyingMethodEnum.SmallestOfMaximum,\
            DefuzzifyingMethodEnum.LargestOfMaximum];
