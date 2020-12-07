from fuzzy_system import FuzzySystem;

from enums.defuzzifying_method_enum import DefuzzifyingMethodEnum;

def main():
    # don't select _None
    defuzzifyingMethod = DefuzzifyingMethodEnum.CentroidOfArea;

    # this does a lot of the set up work to get input into a usable state
    fuzzySystem = FuzzySystem(defuzzifyingMethod);

    fuzzySystem.PrintFclInput();

    fuzzySystem.PlotAntecedents();
    fuzzySystem.PlotConsequents();
    #fuzzySystem.PlotRules();

    # still not sure about these
    fuzzySystem.PrintAntecedentMembershipValues();

    fuzzySystem.PlotDefuzzifiedConsequentValues();

    fuzzySystem.PrintConsequentMembershipValues();

    # last call
    fuzzySystem.ShowPlots();

    input("Press any key to continue . . .");
    return;

# kickstart the app
if __name__ == "__main__":
    main();