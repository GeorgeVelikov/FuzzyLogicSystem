import numpy as np;
import skfuzzy as fuzz;
import skfuzzy.control as ctrl;
import matplotlib.pyplot as plt

from models.rule import Rule;
from models.variable import Variable;
from models.measurement import Measurement;

from enums.defuzzifying_method_enum import DefuzzifyingMethodEnum;

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
        # Keep this as 1
        return 1;

    # constructor
    def __init__(self, defuzzifyingMethod):
        self.DefuzzifyingMethod = defuzzifyingMethod;

        print("Configuring fuzzy rule based system. . .");
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

        self.AntecedentRangesByName = dict();
        self.ConsequentRangesByName = dict();

        self.AntecedentMembershipFunctionsByName = dict();
        self.ConsequentMembershipFunctionsByName = dict();

        self.RulesByRuleBaseName = dict();

        self.ControlSystem = None;
        self.ControlSystemSimulation = None;

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

        self.GetRules();

        self.GetControlSystem();
        self.GetControlSystemSimulation();

    # setup
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
        return self.InputRulesByRuleBaseName;

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
                variables[variableName].append(Variable(line));
            else:
                print("Error: Unhandled scenario for variables.");
                continue;

        self.InputVariableValuesByVariableName = variables;
        return self.InputVariableValuesByVariableName;

    def GetInputMeasurements(self):
        print("Reading measurements. . .");
        measurementLines = self.__ReadDataFile(self.MeasurementsFileName);
        measurements = list();

        for line in measurementLines:
            if not line:
                continue;
            elif "=" in line:
                measurements.append(Measurement(line));
            else:
                print("Error: Unhandled scenario for measurements.");

        self.InputMeasurements = measurements;
        return self.InputMeasurements;

    def GetAntecedentAndConsequentNames(self):
        print("Getting unique antecedents and consequents. . .");
        if (not self.InputRulesByRuleBaseName):
            # no values
            return;

        # get antecedents and consequents names
        for ruleBaseName, ruleBaseRules in self.InputRulesByRuleBaseName.items():

            for rule in ruleBaseRules:
                self.ConsequentNames.add(rule.Result.VariableName);

                for antecedent in rule.Terms:
                    self.AntecedentNames.add(antecedent.VariableName);

        return self.AntecedentNames, self.ConsequentNames;

    def GetRules(self):
        for ruleBaseName, rules in self.InputRulesByRuleBaseName.items():
            self.RulesByRuleBaseName[ruleBaseName] = list();

            for rule in rules:
                # No tokenization, if you have a mish-mash of and/or/anything else, you might get
                # unexpected results. You really shouldn't even try adding brackets in the input.
                # I haven't tested what will happen, but I know it won't work as you expect.
                antecedents = str();
                antecedentsByAntecedentStr = dict();

                for term in rule.Terms:
                    # if variableName is variableValue
                    antecedent = self.AntecedentsByName[term.VariableName][term.VariableValue];

                    # no other obvious way of dealing with N chained connectives and dynamically creating aggregates
                    # use a buffer dict which holds the antecedent based on their str(antecedent) value
                    # we later eval to get the term aggregate. This is a VERY horrible way of doing this
                    # but I couldn't really spot any other way of dealing with this issue other than reflection
                    antecedentStr = str(antecedent);
                    antecedentsByAntecedentStr[antecedentStr] = antecedent;

                    # order is very important, do not change.
                    antecedents += term.LogicalConnective.Operand;
                    antecedents += term.OpeningBrackets;
                    antecedents += term.BooleanOperand;
                    antecedents += 'antecedentsByAntecedentStr["' + antecedentStr + '"]';
                    antecedents += term.ClosingBrackets;

                # then variableName is variableValue
                result = self.ConsequentsByName[rule.Result.VariableName][rule.Result.VariableValue];

                # eval on antecedents creates a potentially complex term aggregate
                fuzzyRule = ctrl.Rule(eval(antecedents), result);

                self.RulesByRuleBaseName[ruleBaseName]\
                    .append(fuzzyRule);

        return self.RulesByRuleBaseName;

    def GetAntecedents(self):
        print("Creating antecedent objects. . .");
        # set antecedents and their ranges
        for name in self.AntecedentNames:
            antecedentValues = self.InputVariableValuesByVariableName[name];

            # TODO: better way of getting min and max?
            antecedentMinValue = min([a.MinValue for a in antecedentValues]);
            antecedentMaxValue = max([a.MaxValue for a in antecedentValues]);

            antecedentValueRange = np.arange(antecedentMinValue, antecedentMaxValue, self.Step);

            self.AntecedentRangesByName[name] = antecedentValueRange;
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

            self.ConsequentRangesByName[name] = consequentValueRange;

            self.ConsequentsByName[name] = ctrl.Consequent(\
                consequentValueRange,\
                name,\
                str(self.DefuzzifyingMethod));

        return self.ConsequentsByName;

    def GetAntecedentMembershipFunctions(self):
        for name in self.AntecedentNames:
            antecedentValues = self.InputVariableValuesByVariableName[name];
            antecedent = self.AntecedentsByName[name];
            self.AntecedentMembershipFunctionsByName[name] = dict();

            for antecedentValue in antecedentValues:
                # will always be 4tuple input => always have a trapezoidal mf
                trapezoidalMembershipFunction = fuzz.trapmf(\
                    antecedent.universe,\
                    antecedentValue.TrapezoidalInput);

                # set up each antecedent value name and membership function
                antecedent[antecedentValue.Name] = trapezoidalMembershipFunction;
                self.AntecedentMembershipFunctionsByName[name][antecedentValue.Name] =\
                    trapezoidalMembershipFunction;

        return self.AntecedentMembershipFunctionsByName;

    def GetConsequentMembershipFunctions(self):
        for name in self.ConsequentNames:
            consequentValues = self.InputVariableValuesByVariableName[name];
            consequent = self.ConsequentsByName[name];
            self.ConsequentMembershipFunctionsByName[name] = dict();

            for consequentValue in consequentValues:
                # will always be 4tuple input => always have a trapezoidal mf
                trapezoidalMembershipFunction = fuzz.trapmf(\
                    consequent.universe,\
                    consequentValue.TrapezoidalInput);

                consequent[consequentValue.Name] = trapezoidalMembershipFunction;
                self.ConsequentMembershipFunctionsByName[name][consequentValue.Name] =\
                   trapezoidalMembershipFunction;

        return self.ConsequentMembershipFunctionsByName;

    def GetControlSystem(self):
        allRules = self.RulesByRuleBaseName.values();

        # flattening all of the potential rulebase rules. Not sure if this is semantically
        # correct. I don't see any reason as to why we cannot apply multiple rule bases.
        flatAllRules = [rule for ruleBaseRules in allRules for rule in ruleBaseRules];

        self.ControlSystem = ctrl.ControlSystem(flatAllRules);

        return self.ControlSystem;

    def GetControlSystemSimulation(self):
        self.ControlSystemSimulation = ctrl.ControlSystemSimulation(self.ControlSystem);

        for measurement in self.InputMeasurements:
            self.ControlSystemSimulation\
                .input[measurement.Name] = measurement.Value;

        self.ControlSystemSimulation.compute();

        return self.ControlSystemSimulation;

    # helper
    def __ReadDataFile(self, fileName):
        return open("data/" + fileName)\
            .read()\
            .splitlines();

    # output
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

        return;

    def PrintAntecedentMembershipValues(self):
        print("\nAntecedent Membership Values:");
        for name in self.AntecedentNames:
            print("\n\t" + name);

            antecedentValues = self.AntecedentMembershipFunctionsByName[name];
            input = next(measurement.Value for measurement in self.InputMeasurements if measurement.Name == name)

            for variableName, trapezoidalMembershipFunction in antecedentValues.items():
                fuzzyOutputForValue = trapezoidalMembershipFunction[input]
                print("\t\t"+ variableName + " = " + str(fuzzyOutputForValue))
        return;

    def PrintConsequentMembershipValues(self):
        print("\nConsequent Membership Values:");
        for name in self.ConsequentNames:
            print("\t" + name);

            consequentValues = self.ConsequentMembershipFunctionsByName[name];
            # rounding because our consequent value is never an int
            output = round(self.ControlSystemSimulation.output[name]);

            for variableName, trapezoidalMembershipFunction in consequentValues.items():
                fuzzyOutputForValue = trapezoidalMembershipFunction[output]
                print("\t\t"+ variableName + " = " + str(fuzzyOutputForValue))
        return;

    def PlotDefuzzifiedConsequentValues(self):
        print("\nUsing the " + self.DefuzzifyingMethod.Name + " defuzzifying method.")
        print("\nDefuzzified Consequent Values:");
        for name, consequent in self.ConsequentsByName.items():
            consequent.view(sim = self.ControlSystemSimulation);
            consequentValue = self.ControlSystemSimulation.output[name];
            print("\t" + name + " = " + str(consequentValue));
        return;

    def PlotAntecedents(self):
        # placeholder, just wanting to test whether the membership functions are correct
        for antecedentName, antecedent in self.AntecedentsByName.items():
            antecedent.view();
        return;

    def PlotConsequents(self):
        for consequentName, consequent in self.ConsequentsByName.items():
            consequent.view();
        return;

    def PlotRules(self):
        # plot the rules - they're really not that helpful as they are not notated
        # it is interesting to see how scikit fuzzy internally graphs them out though
        for ruleBaseName, rules in self.RulesByRuleBaseName.items():
            for rule in rules:
                rule.view();
        return;

    def ShowPlots(self):
        # you need to call matplotlib.show because scikit fuzzy relies on it and can't
        # really tell whenever we are ready with calling .view(). If we don't call .show()
        # we will get a bunch of "hanging" windows.
        # https://stackoverflow.com/a/60235346
        print("\nMatplotlib running on the UI thread. Close all graphs to continue. . .");
        plt.show();
        print("All graphs closed. Continuing. . .");
        return;