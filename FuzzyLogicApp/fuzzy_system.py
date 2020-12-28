# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆
# 🦆     Georgi Velikov     🦆
# 🦆        51660024        🦆
# 🦆 University Of Aberdeen 🦆
# 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆

import numpy as np;
import skfuzzy as fuzz;
import skfuzzy.control as ctrl;
import matplotlib.pyplot as plt

from fcl_parser import FclParser;

from enums.defuzzifying_method_enum import DefuzzifyingMethodEnum;

class FuzzySystem():
    def Step(self, deltaMaxMin):
        if (deltaMaxMin >= 100):
            return 1;
        else:
            return deltaMaxMin / 1000.0;

    # constructor
    def __init__(self, defuzzifyingMethod):
        self.Parser = FclParser();
        self.DefaultDefuzzifyingMethod = defuzzifyingMethod;

        print("\nUsing the " + self.DefaultDefuzzifyingMethod.Name + " defuzzifying method for graphs.");

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

        self.__Load();

    def __Load(self):
        # actual setup, not actually used as getters as they set the instance variables within the calls
        # whilst likely not semantically correct to be called a getter, I use this as a form of 'typing'
        # so that the variables can be easily identified type-wise
        self.InputRulesByRuleBaseName = self.Parser.GetInputRules();
        self.InputVariableValuesByVariableName = self.Parser.GetInputVariables();
        self.InputMeasurements = self.Parser.GetInputMeasurements();

        self.GetAntecedentNames();
        self.GetConsequentNames();

        self.GetAntecedents();
        self.GetConsequents();

        self.GetAntecedentMembershipFunctions();
        self.GetConsequentMembershipFunctions();

        self.GetRules();

        self.GetControlSystem();
        self.GetControlSystemSimulation();
        return;

    # various setup calls
    def GetAntecedentNames(self):
        print("Getting unique Consequents. . .");
        if (not self.InputRulesByRuleBaseName):
            # no values
            return;

        # get antecedents names
        for ruleBaseName, ruleBaseRules in self.InputRulesByRuleBaseName.items():
            for rule in ruleBaseRules:
                for antecedent in rule.Terms:
                    self.AntecedentNames.add(antecedent.VariableName);

        return self.AntecedentNames;

    def GetConsequentNames(self):
        print("Getting unique Antecedents. . .");
        if (not self.InputRulesByRuleBaseName):
            # no values
            return;

        for ruleBaseName, ruleBaseRules in self.InputRulesByRuleBaseName.items():
            for rule in ruleBaseRules:
                self.ConsequentNames.add(rule.Result.VariableName);

        return self.ConsequentNames;

    def GetAntecedents(self):
        print("Creating Antecedents. . .");
        # set antecedents and their ranges
        for name in self.AntecedentNames:
            antecedentValues = self.InputVariableValuesByVariableName[name];

            # TODO: better way of getting min and max?
            antecedentMinValue = min([a.MinValue for a in antecedentValues]);
            antecedentMaxValue = max([a.MaxValue for a in antecedentValues]);

            delta = antecedentMaxValue - antecedentMinValue;

            # off by one errors are one of the 3 hardest problems in computing science
            antecedentValueRange = np.arange(\
                antecedentMinValue, \
                antecedentMaxValue + self.Step(delta), \
                self.Step(delta));

            self.AntecedentRangesByName[name] = antecedentValueRange;
            self.AntecedentsByName[name] = ctrl.Antecedent(antecedentValueRange, name);

        return self.AntecedentsByName;

    def GetConsequents(self):
        print("Creating Consequents. . .");
        # set consequents and their ranges
        for name in self.ConsequentNames:
            consequentValues = self.InputVariableValuesByVariableName[name];

            # TODO: better way of getting min and max?
            consequentMinValue = min([c.MinValue for c in consequentValues]);
            consequentMaxValue = max([c.MaxValue for c in consequentValues]);

            delta = consequentMaxValue - consequentMinValue;

            # off by one errors are one of the 3 hardest problems in computing science
            consequentValueRange = np.arange(\
                consequentMinValue, \
                consequentMaxValue + self.Step(delta), \
                self.Step(delta));

            self.ConsequentRangesByName[name] = consequentValueRange;

            self.ConsequentsByName[name] = ctrl.Consequent(\
                consequentValueRange,\
                name,\
                str(self.DefaultDefuzzifyingMethod));

        return self.ConsequentsByName;

    def GetRules(self):
        print("Creating Fuzzy Rules. . .");
        for ruleBaseName, rules in self.InputRulesByRuleBaseName.items():
            self.RulesByRuleBaseName[ruleBaseName] = dict();

            for rule in rules:
                # No tokenization, if you have a mish-mash of and/or/anything else, you might get unexpected results.
                antecedentsTermAggregate = str();
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
                    antecedentsTermAggregate += \
                        term.LogicalConnective.Operand +\
                        term.OpeningParentheses +\
                        term.BooleanOperand +\
                        'antecedentsByAntecedentStr["' + antecedentStr + '"]' +\
                        term.ClosingParentheses;

                # then variableName is variableValue
                result = self.ConsequentsByName[rule.Result.VariableName][rule.Result.VariableValue];

                # eval on antecedents creates a potentially complex term aggregate
                fuzzyRule = ctrl.Rule(eval(antecedentsTermAggregate), result);

                self.RulesByRuleBaseName[ruleBaseName][rule.Name] = fuzzyRule;

        return self.RulesByRuleBaseName;

    def GetAntecedentMembershipFunctions(self):
        print("Creating Antecedent membership functions. . .");
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
        print("Creating Consequent membership functions. . .");
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
        print("Creating Control System and importing Fuzzy Rules. . .");
        flatRules = list();

        # flattening all of the potential rulebase rules. Not sure if this is semantically
        # correct. I don't see any reason as to why we cannot apply multiple rule bases.
        for ruleBaseName, ruleKvp in self.RulesByRuleBaseName.items():
            for ruleName, rule in ruleKvp.items():
                flatRules.append(rule);

        self.ControlSystem = ctrl.ControlSystem(flatRules);

        return self.ControlSystem;

    def GetControlSystemSimulation(self):
        self.ControlSystemSimulation = ctrl.ControlSystemSimulation(self.ControlSystem);

        for measurement in self.InputMeasurements:
            self.ControlSystemSimulation\
                .input[measurement.Name] = measurement.Value;

        self.ControlSystemSimulation.compute();

        return self.ControlSystemSimulation;

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

    def PrintAntecedentMembershipDegrees(self):
        print("\nAntecedent Membership Degrees:");
        for name, antecedent in self.AntecedentsByName.items():
            print("\n\t" + name);

            antecedentValues = self.AntecedentMembershipFunctionsByName[name];
            input = next(measurement.Value for measurement in self.InputMeasurements if measurement.Name == name)

            for variableName, trapezoidalMembershipFunction in antecedentValues.items():
                degreeOfMembership = fuzz.interp_membership(\
                        antecedent.universe, \
                        trapezoidalMembershipFunction, \
                        input);

                print("\t\t"+ variableName + " = " + str(degreeOfMembership))
        return;

    def PrintConsequentMembershipDegrees(self):
        print("\nConsequent Membership Degrees:");
        self.GetControlSystemSimulation();
        for name, consequent in self.ConsequentsByName.items():
            print("\t" + name);

            for valueName, term in consequent.terms.items():
                print("\t\t" + valueName + " = " + str(term._cut))
        return;

    def PlotDefuzzifiedConsequentValues(self):
        print("\nDefuzzified Consequent Values:");
        for name, consequent in self.ConsequentsByName.items():
            print("\t" + name);

            for method in DefuzzifyingMethodEnum.Values():
                consequent.defuzzify_method = str(method);
                self.GetControlSystemSimulation();
                consequent.view(sim = self.ControlSystemSimulation);
                plt.title(name + " - " + method.Name);
                consequentValue = self.ControlSystemSimulation.output[name];

                print("\t\t" + method.Name + " - " + str(consequentValue));

            consequent.defuzzify_method = str(self.DefaultDefuzzifyingMethod);
            self.GetControlSystemSimulation();
        return;

    def PlotAntecedents(self):
        # placeholder, just wanting to test whether the membership functions are correct
        for antecedentName, antecedent in self.AntecedentsByName.items():
            antecedent.view();
            plt.title("Antecedent - " + antecedentName);
        return;

    def PlotConsequents(self):
        for consequentName, consequent in self.ConsequentsByName.items():
            consequent.view();
            plt.title("Consequent - " + consequentName);
        return;

    def PlotRules(self):
        # plot the rules - they're really not that helpful as they are not notated
        # it is interesting to see how scikit fuzzy internally graphs them out though
        for ruleBaseName, rules in self.RulesByRuleBaseName.items():
            for ruleName, rule in rules.items():
                rule.view();
                plt.title("Rule base - " + ruleBaseName + "\nRule - " + ruleName);
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