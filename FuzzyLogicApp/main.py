from fuzzy_system import FuzzySystem;
from defuzzifying_method_enum import DefuzzifyingMethodEnum;

def main():
    # this does a lot of the set up work to get input into a usable state
    deffuzifyingMethod = DefuzzifyingMethodEnum.BisectorOfArea;

    fuzzySystem = FuzzySystem(deffuzifyingMethod);

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