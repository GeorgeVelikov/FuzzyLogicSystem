from configuration import Configuration;

def main():
    # this does a lot of the set up work to get input into a usable state
    configuration = Configuration();

    configuration.PrintFclInput();

    input("Press any key to continue . . .");
    return;

# kickstart the app
if __name__ == "__main__":
    main();