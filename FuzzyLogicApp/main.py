from fuzzy_system import FuzzySystem;

from enums.defuzzifying_method_enum import DefuzzifyingMethodEnum;

def main():
    # don't select _None, the system will do the 5 methods supported by scikit-fuzzy.
    # This is just a default value in the case of adding new functionality. More of a sanity check!
    # Used for the graphs
    defaultDefuzzifyingMethod = DefuzzifyingMethodEnum.CentroidOfArea;

    # this does a lot of the set up work to get input into a usable state
    fuzzySystem = FuzzySystem(defaultDefuzzifyingMethod);

    fuzzySystem.PrintFclInput();

    fuzzySystem.PlotAntecedents();
    fuzzySystem.PlotConsequents();
    #fuzzySystem.PlotRules();

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