from fuzzy_system import FuzzySystem;

def main():
    # this does a lot of the set up work to get input into a usable state
    fuzzySystem = FuzzySystem();

    fuzzySystem.PrintFclInput();

    fuzzySystem.PrintDefuzzifiedAntecedentMembershipFunctions();
    fuzzySystem.PrintDefuzzifiedConsequentMembershipFunctions();

    fuzzySystem.PlotAntecedents();
    fuzzySystem.PlotConsequents();
    #fuzzySystem.PlotRules();
    fuzzySystem.PlotDefuzzifiedConsequentValues();

    fuzzySystem.ShowPlots();

    input("Press any key to continue . . .");
    return;

# kickstart the app
if __name__ == "__main__":
    main();