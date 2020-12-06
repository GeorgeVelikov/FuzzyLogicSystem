from configuration import Configuration;

def main():
    # this does a lot of the set up work to get input into a usable state
    configuration = Configuration();

    configuration.PrintFclInput();

    input("Press any key to continue . . .");
    return;

#Ignore this spaghetti, will get used later in some form in the Configuration class
#for antecedentValue in antecedentValues:
#    tupleRange = np.arange(\
#        antecedentValue.A - antecedentValue.Alpha,\
#        antecedentValue.B + antecedentValue.Beta,\
#        1);

#    # will always be 4tuple input => always have a trapezoidal mf
#    trapezoidalMembershipFunction = fuzz.trapmf(tupleRange, antecedentValue.TrapezoidalInput);

# kickstart the app
if __name__ == "__main__":
    main();