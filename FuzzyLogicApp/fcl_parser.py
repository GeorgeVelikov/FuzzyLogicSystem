import re;

from models.rule import Rule;
from models.term import Term;
from models.variable import Variable;
from models.measurement import Measurement;

from enums.logical_connective_enum import LogicalConnectiveEnum;

class FclParser:
    # constants
    __InputFileName = "input.txt";

    def __init__(self):
        self.RuleBaseName = str();
        self.AllLines = list();
        self.RuleLines = list();
        self.VariableLines = list();
        self.MeasurementLines = list();

        self.__ReadInputFile();

    # line parsing of each and outputting the resulting abstractions
    def GetInputRules(self):
        print("Reading rules. . .");
        rules = dict();
        rules[self.RuleBaseName] = list();

        for line in self.RuleLines:
            if not line:
                continue;
            elif self.RuleBaseName and line:
                rule = self.CreateRule(line);
                rules[self.RuleBaseName]\
                    .append(rule);
            else:
                print("Error: Unhandled scenario for rules.");
                continue;

        return rules;

    def GetInputVariables(self):
        print("Reading variables. . .");
        variables = dict();
        variableName = str();

        for line in self.VariableLines:
            if not line:
                continue;
            elif not any(map(str.isdigit, line)):
                variableName = line;
                variables[variableName] = [];
            elif variableName and line:
                variable = self.CreateVariable(line);
                variables[variableName]\
                    .append(variable);
            else:
                print("Error: Unhandled scenario for variables.");
                continue;

        return variables;

    def GetInputMeasurements(self):
        print("Reading measurements. . .");
        measurements = list();

        for line in self.MeasurementLines:
            if not line:
                continue;
            elif "=" in line:
                measurement = self.CreateMeasurement(line);
                measurements.append(measurement);
            else:
                print("Error: Unhandled scenario for measurements.");

        return measurements;

    # abstraction creation
    def CreateMeasurement(self, measurementText):
        name = measurementText\
            .split("=")[0]\
            .strip();

        value = measurementText\
            .split("=")[1]\
            .strip()\
            .split(" ")[0]\
            .strip();

        evalValue = eval(value);

        return Measurement(name, evalValue);

    def CreateVariable(self, variableText):
        name = variableText\
            .split(" ")[0]\
            .strip();

        # maybe a bit overzealous, but I can see how [A, B, Alpha, Beta] makes sense
        tuple = variableText\
            .split(" ", 1)[-1]\
            .replace("[", "")\
            .replace("]", "")\
            .strip();

        if "," not in tuple:
            tuple = tuple\
                .replace(" ", ",");

        evalTuple = eval(tuple);

        return Variable(name, evalTuple);

    def CreateRule(self, ruleText):
        name = str();
        terms = list(); # List of Terms
        result = None; # Term type

        ruleLine = ruleText

        self.__CheckRuleLineIsValid(ruleLine);

        # get rule name
        ruleName = ruleLine\
            .split(":")[0]\
            .strip()

        name = ruleName;

        # remove parsed data rule name
        ruleLine = re.split(" if ", ruleLine, flags=re.IGNORECASE)[1]\
            .strip();

        firstTerm = self.CreateTerm(ruleLine);
        firstTerm.LogicalConnective = LogicalConnectiveEnum.If;
        terms.append(firstTerm);

        # remove parsed initial term
        ruleLine = " " + ruleLine\
            .split(firstTerm.VariableValue)[1][firstTerm.ClosingBracketsCount:]\
            .strip();

        # get result text
        resultText = re.split(" then ", ruleLine, flags=re.IGNORECASE)[1]\
            .strip();

        result = self.CreateTerm(resultText);
        result.LogicalConnective = LogicalConnectiveEnum.Then;

        # remove result text, add a white space to make the replace symmetric
        # this just makes sure we replace and
        ruleLine = " " + re.split(" then ", ruleLine, flags=re.IGNORECASE)[0]\
            .strip();

        if not ruleLine.strip():
            # we dont have chained antecedents, break earlier
            rule = Rule(name, terms, result);
            return rule;

        # chained and/or connectives, this is just a hacky way of making sure
        # we split all connectives.
        # this however might break on unknown connectives.
        chainedTerms = ruleLine\
            .replace(" and ", "#and# ")\
            .replace(" or ", " #or# ")\
            .split("#");

        # safely remove all nones and white space
        whiteSpaceInTerms = [term for term in chainedTerms if (term.isspace() or not term)];

        for whiteSpace in whiteSpaceInTerms:
            chainedTerms.remove(whiteSpace);

        # add subsequent terms
        for i in range(0, len(chainedTerms), 2):
            connectiveText = chainedTerms[i]\
                .strip();

            termText = chainedTerms[i + 1];

            logicalConnective = \
                LogicalConnectiveEnum.And if connectiveText == str(LogicalConnectiveEnum.And) \
                else LogicalConnectiveEnum.Or if connectiveText == str(LogicalConnectiveEnum.Or) \
                else LogicalConnectiveEnum._None;

            if (logicalConnective == LogicalConnectiveEnum._None):
                # something not right, cannot have subsequent terms with
                # None or unknown connectives
                print("Incorrect Logical Connective used for subsequent term - ", chainedVariableConnectiveText);
                continue

            chainedTerm = self.CreateTerm(termText);
            chainedTerm.LogicalConnective = logicalConnective;

            terms.append(chainedTerm);

        rule = Rule(name, terms, result);
        return rule;

    def CreateTerm(self, termText):
        variableName = str();
        variableValue = str();
        isNegated = False;
        openingBracketsCount = 0;
        closingBracketsCount = 0;

        variableName = re.split(" is ", termText, flags=re.IGNORECASE)[0]\
            .strip()

        if "(" in variableName:
            openingBracketsCount = variableName.count("(");
            variableName = variableName.replace("(", str());

        variableValue = re.split(" is ", termText, flags=re.IGNORECASE)[1]\
            .strip()\
            .split(" ")[0]\
            .strip();

        if "not" in variableValue:
            variableValue = re.split(" is ", termText, flags=re.IGNORECASE)[1]\
                .strip()\
                .split(" ")[1]\
                .strip()
            isNegated = True;

        if ")" in variableValue:
            closingBracketsCount = variableValue.count(")");
            variableValue = variableValue.replace(")", str());

        term = Term(\
            LogicalConnectiveEnum._None,\
            isNegated,\
            openingBracketsCount,\
            closingBracketsCount,\
            variableName,\
            variableValue);

        return term;

    # helper
    def __ReadInputFile(self, filename = None):
        # clean up if re-used
        self.RuleBaseName = str();
        self.AllLines = list();
        self.RuleLines = list();
        self.VariableLines = list();
        self.MeasurementLines = list();

        if not filename:
            filename = self.__InputFileName;

        with open(filename, "r") as inputFile:
            self.AllLines = [line.strip() for line in inputFile.readlines() if not line.isspace()]

            if not self.AllLines:
                raise Exception("Invalid input file");

            self.RuleBaseName = self.AllLines[0]\
                .strip();

            for line in self.AllLines[1:]:
                if ":" in line:
                    self.RuleLines\
                        .append(line);
                elif "=" in line:
                    self.MeasurementLines\
                        .append(line);
                else:
                    # Dodgy, but no other way of dealing with the input
                    self.VariableLines\
                        .append(line);

        return self.AllLines;

    # validation
    def __CheckRuleLineIsValid(self, ruleLine):
        if ruleLine.count("(") != ruleLine.count(")"):
            raise Exception("Invalid number of brackets used. Please make sure all brackets are matched.");
            return False;

        return True;