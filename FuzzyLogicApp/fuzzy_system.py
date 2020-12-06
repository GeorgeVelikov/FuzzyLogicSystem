import numpy as np;
import skfuzzy as fuzz;
import skfuzzy.control as ctrl;
import matplotlib.pyplot as plt

from rule import Rule;
from variable_value import VariableValue;
from variable_measurement import VariableMeasurement;

class FuzzySystem():
    # constants
    @property
    def RulesFileName(self):
       return "rules.txt";

    @property
    def MeasurementsFileName(self):
       return "measurements.txt";

    @property
    def VariablesFileName(self):
       return "variables.txt";

    @property
    def Step(self):
        # TODO: step is 1 atm, do we want it to be more accurate?
        return 1;

    # constructor
    def __init__(self):
        print("Configuring fuzzy rule based system. . .");
        # instance variables
        # using this as a hint to what each instance variable is since Python isn't strongly typed

        # input values
        self.InputRulesByRuleBaseName = dict();
        self.InputVariableValuesByVariableName = dict();
        self.InputMeasurements = list();

        # actual fuzzy system values
        self.AntecedentNames = set();
        self.ConsequentNames = set();
        self.AntecedentsByName = dict();
        self.ConsequentsByName = dict();
        self.AntecedentMembershipFunctionsByName = dict();
        self.ConsequentMembershipFunctionsByName = dict();

        # actual setup, not actually used as getters as they set the instance variables within the calls
        # whilst likely not semantically correct to be called a getter, I use this as a form of 'typing'
        # so that the variables can be easily identified type-wise
        self.GetInputRules();
        self.GetInputVariables();
        self.GetInputMeasurements();

        self.GetAntecedentAndConsequentNames();
        self.GetAntecedents();
        self.GetConsequents();
        self.GetAntecedentMembershipFunctions();
        self.GetConsequentMembershipFunctions();

    # set up
    def GetInputRules(self):
        print("Reading rules. . .");
        ruleLines = self.__ReadDataFile(self.RulesFileName);
        rules = dict();
        ruleBaseName = str();

        for line in ruleLines:
            if not line:
                continue;
            elif ":" not in line:
                ruleBaseName = line;
                rules[ruleBaseName] = list();
            elif ruleBaseName and line:
                rules[ruleBaseName].append(Rule(line));
            else:
                print("Error: Unhandled scenario for rules.");
                continue;

        self.InputRulesByRuleBaseName = rules;
        return rules;

    def GetInputVariables(self):
        print("Reading variables. . .");
        variableLines = self.__ReadDataFile(self.VariablesFileName);
        variables = dict();
        variableName = str();

        for line in variableLines:
            if not line:
                continue;
            elif not any(map(str.isdigit, line)):
                variableName = line;
                variables[variableName] = [];
            elif variableName and line:
                variables[variableName].append(VariableValue(line));
            else:
                print("Error: Unhandled scenario for variables.");
                continue;

        self.InputVariableValuesByVariableName = variables;
        return variables;

    def GetInputMeasurements(self):
        print("Reading measurements. . .");
        measurementLines = self.__ReadDataFile(self.MeasurementsFileName);
        measurements = list();

        for line in measurementLines:
            if not line:
                continue;
            elif "=" in line:
                measurements.append(VariableMeasurement(line));
            else:
                print("Error: Unhandled scenario for measurements.");

        self.InputMeasurements = measurements;
        return measurements;

    def GetAntecedentAndConsequentNames(self):
        print("Getting unique antecedents and consequents. . .");
        if (not self.InputRulesByRuleBaseName):
            # no values
            return;

        # get antecedents and consequents names
        for ruleBaseName, ruleBaseRules in self.InputRulesByRuleBaseName.items():

            for rule in ruleBaseRules:
                self.ConsequentNames.add(rule.Result.VariableName);

                for antecedent in rule.Conditions:
                    self.AntecedentNames.add(antecedent.VariableName);

        return self.AntecedentNames, self.ConsequentNames;

    def GetAntecedents(self):
        print("Creating antecedent objects. . .");
        # set antecedents and their ranges
        for name in self.AntecedentNames:
            antecedentValues = self.InputVariableValuesByVariableName[name];

            # TODO: better way of getting min and max?
            antecedentMinValue = min([a.MinValue for a in antecedentValues]);
            antecedentMaxValue = max([a.MaxValue for a in antecedentValues]);

            antecedentValueRange = np.arange(antecedentMinValue, antecedentMaxValue, self.Step);

            self.AntecedentsByName[name] = ctrl.Antecedent(antecedentValueRange, name);

        return self.AntecedentsByName;

    def GetConsequents(self):
        print("Creating consequent objects. . .");
        # set consequents and their ranges
        for name in self.ConsequentNames:
            consequentValues = self.InputVariableValuesByVariableName[name];

            # TODO: better way of getting min and max?
            consequentMinValue = min([c.MinValue for c in consequentValues]);
            consequentMaxValue = max([c.MaxValue for c in consequentValues]);

            consequentValueRange = np.arange(consequentMinValue, consequentMaxValue, self.Step);

            self.ConsequentsByName[name] = ctrl.Consequent(consequentValueRange, name);

        return self.ConsequentsByName;

    def GetAntecedentMembershipFunctions(self):
        for name in self.AntecedentNames:
            antecedentValues = self.InputVariableValuesByVariableName[name];
            antecedent = self.AntecedentsByName[name];
            self.AntecedentMembershipFunctionsByName[name] = list();

            for antecedentValue in antecedentValues:
                # will always be 4tuple input => always have a trapezoidal mf
                trapezoidalMembershipFunction = fuzz.trapmf(\
                    antecedent.universe,\
                    antecedentValue.TrapezoidalInput);

                # set up each antecedent value name and membership function
                antecedent[antecedentValue.Name] = trapezoidalMembershipFunction;

                self.AntecedentMembershipFunctionsByName[name]\
                    .append(trapezoidalMembershipFunction);

        return self.AntecedentMembershipFunctionsByName;

    def GetConsequentMembershipFunctions(self):
        for name in self.ConsequentNames:
            consequentValues = self.InputVariableValuesByVariableName[name];
            consequent = self.ConsequentsByName[name];
            self.ConsequentMembershipFunctionsByName[name] = list();

            for consequentValue in consequentValues:
                # will always be 4tuple input => always have a trapezoidal mf
                trapezoidalMembershipFunction = fuzz.trapmf(\
                    consequent.universe,\
                    consequentValue.TrapezoidalInput);

                consequent[consequentValue.Name] = trapezoidalMembershipFunction;

                self.ConsequentMembershipFunctionsByName[name]\
                    .append(trapezoidalMembershipFunction);

        return self.ConsequentMembershipFunctionsByName;

    # helper
    def __ReadDataFile(self, fileName):
        return open("data/" + fileName)\
            .read()\
            .splitlines();

    def PrintFclInput(self):
        for ruleBaseName, ruleBaseRules in self.InputRulesByRuleBaseName.items():
            print ("\nRule base - " + ruleBaseName + ":");
            for rule in ruleBaseRules:
                print(rule);

        for variableName, variableValues in self.InputVariableValuesByVariableName.items():
            print ("\nVariable - " + variableName + ":");
            for value in variableValues:
                print(value);

        print("\nMeasurements:")
        for measurement in self.InputMeasurements:
            print(measurement);

    def GraphTest(self):
        # placeholder, just wanting to test whether the membership functions are correct
        for antecedentName, antecedent in self.AntecedentsByName.items():
            antecedent.view();

        for consequentName, consequent in self.ConsequentsByName.items():
            consequent.view();

        plt.show()
