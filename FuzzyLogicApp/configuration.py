import numpy as np;
import skfuzzy as fuzz;
import skfuzzy.control as ctrl;

from rule import Rule;
from variable_value import VariableValue;
from variable_measurement import VariableMeasurement;

class Configuration():
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
        self.Rules = dict();
        self.Variables = dict();
        self.Measurements = list();

        self.AntecedentNames = set();
        self.ConsequentNames = set();
        self.Antecedents = dict();
        self.Consequents = dict();
        self.AntecedentMembershipFunctions = dict();
        self.ConsequentMembershipFunctions = dict();

        # actual setup, not actually used as getters as they set the instance variables within the calls
        # whilst likely not semantically correct to be called a getter, I use this as a form of 'typing'
        # so that the variables can be easily identified type-wise
        self.GetRules();
        self.GetVariables();
        self.GetMeasurements();

        self.GetAntecedentAndConsequentNames();
        self.GetAntecedents();
        self.GetConsequents();
        self.GetAntecedentMembershipFunctions();
        self.GetConsequentMembershipFunctions();

    # set up
    def GetRules(self):
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

        self.Rules = rules;
        return rules;

    def GetVariables(self):
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

        self.Variables = variables;
        return variables;

    def GetMeasurements(self):
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

        self.Measurements = measurements;
        return measurements;

    def GetAntecedentAndConsequentNames(self):
        print("Getting unique antecedents and consequents. . .");
        if (not self.Rules):
            # no values
            return;

        # get antecedents and consequents names
        for ruleBaseName, ruleBaseRules in self.Rules.items():

            for rule in ruleBaseRules:
                self.ConsequentNames.add(rule.Result.VariableName);

                for antecedent in rule.Conditions:
                    self.AntecedentNames.add(antecedent.VariableName);

        return self.AntecedentNames, self.ConsequentNames;

    def GetAntecedents(self):
        print("Creating antecedent objects. . .");
        # set antecedents and their ranges
        for name in self.AntecedentNames:
            antecedentValues = self.Variables[name];

            # TODO: better way of getting min and max?
            antecedentMinValue = min([a.MinValue for a in antecedentValues]);
            antecedentMaxValue = max([a.MaxValue for a in antecedentValues]);

            antecedentValueRange = np.arange(antecedentMinValue, antecedentMaxValue, self.Step);

            self.Antecedents[name] = ctrl.Antecedent(antecedentValueRange, name);

        return self.Antecedents;

    def GetConsequents(self):
        print("Creating consequent objects. . .");
        # set consequents and their ranges
        for name in self.ConsequentNames:
            consequentValues = self.Variables[name];

            # TODO: better way of getting min and max?
            consequentMinValue = min([c.MinValue for c in consequentValues]);
            consequentMaxValue = max([c.MaxValue for c in consequentValues]);

            consequentValueRange = np.arange(consequentMinValue, consequentMaxValue, self.Step);

            self.Consequents[name] = ctrl.Consequent(consequentValueRange, name);

        return self.Consequents;

    def GetAntecedentMembershipFunctions(self):
        for name in self.AntecedentNames:
            antecedentValues = self.Variables[name];
            antecedent = self.Antecedents[name];
            self.AntecedentMembershipFunctions[name] = list();

            for antecedentValue in antecedentValues:
                # will always be 4tuple input => always have a trapezoidal mf
                trapezoidalMembershipFunction = fuzz.trapmf(\
                    antecedent.universe,\
                    antecedentValue.TrapezoidalInput);

                # set up each antecedent value name and membership function
                antecedent[antecedentValue.Name] = trapezoidalMembershipFunction;
                self.AntecedentMembershipFunctions[name].append(trapezoidalMembershipFunction);

        return self.AntecedentMembershipFunctions;

    def GetConsequentMembershipFunctions(self):
        for name in self.AntecedentNames:
            consequentValues = self.Variables[name];
            consequent = self.Consequents[name];
            self.ConsequentMembershipFunctions[name] = list();

            for consequentValue in consequentValues:
                # will always be 4tuple input => always have a trapezoidal mf
                trapezoidalMembershipFunction = fuzz.trapmf(\
                    consequent.universe,\
                    consequentValue.TrapezoidalInput);

                consequent[consequentValue.Name] = trapezoidalMembershipFunction;
                self.ConsequentMembershipFunctions[name].append(trapezoidalMembershipFunction);

        return self.ConsequentMembershipFunctions;

    # helper
    def __ReadDataFile(self, fileName):
        return open("data/" + fileName)\
            .read()\
            .splitlines();

    def PrintFclInput(self):
        for ruleBaseName, ruleBaseRules in self.Rules.items():
            print ("\nRule base - " + ruleBaseName + ":");
            for rule in ruleBaseRules:
                print(rule);

        for variableName, variableValues in self.Variables.items():
            print ("\nVariable - " + variableName + ":");
            for value in variableValues:
                print(value);

        print("\nMeasurements:")
        for measurement in self.Measurements:
            print(measurement);
