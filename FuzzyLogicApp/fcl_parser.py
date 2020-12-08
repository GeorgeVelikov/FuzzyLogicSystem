from models.rule import Rule;
from models.term import Term;
from models.variable import Variable;
from models.measurement import Measurement;

from enums.logical_connective_enum import LogicalConnectiveEnum;

class FclParser:
    # constants
    __RulesFileName ="rules.txt";
    __MeasurementsFileName = "measurements.txt";
    __VariablesFileName = "variables.txt";

    # line parsing of each and outputting the resulting abstractions
    def GetInputRules():
        print("Reading rules. . .");
        ruleLines = FclParser.__ReadDataFile(FclParser.__RulesFileName);
        rules = dict();
        ruleBaseName = str();

        for line in ruleLines:
            if not line:
                continue;
            elif ":" not in line:
                ruleBaseName = line;
                rules[ruleBaseName] = list();
            elif ruleBaseName and line:
                rule = FclParser.CreateRule(line);
                rules[ruleBaseName].append(rule);
            else:
                print("Error: Unhandled scenario for rules.");
                continue;

        return rules;

    def GetInputVariables():
        print("Reading variables. . .");
        variableLines = FclParser.__ReadDataFile(FclParser.__VariablesFileName);
        variables = dict();
        variableName = str();

        for line in variableLines:
            if not line:
                continue;
            elif not any(map(str.isdigit, line)):
                variableName = line;
                variables[variableName] = [];
            elif variableName and line:
                variable = FclParser.CreateVariable(line);
                variables[variableName].append(variable);
            else:
                print("Error: Unhandled scenario for variables.");
                continue;

        return variables;

    def GetInputMeasurements():
        print("Reading measurements. . .");
        measurementLines = FclParser.__ReadDataFile(FclParser.__MeasurementsFileName);
        measurements = list();

        for line in measurementLines:
            if not line:
                continue;
            elif "=" in line:
                measurement = FclParser.CreateMeasurement(line);
                measurements.append(measurement);
            else:
                print("Error: Unhandled scenario for measurements.");

        return measurements;

    # abstraction creation
    def CreateMeasurement(measurementText):
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

    def CreateVariable(variableText):
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

    def CreateRule(ruleText):
        name = str();
        terms = list(); # List of Terms
        result = None; # Term type

        ruleLine = ruleText.lower()

        FclParser.__CheckRuleLineIsValid(ruleLine);

        # get rule name
        ruleName = ruleLine\
            .split(":")[0]\
            .strip()

        name = ruleName;

        # remove parsed data rule name
        ruleLine = ruleLine\
            .split("if ")[1]\
            .strip();

        firstTerm = FclParser.CreateTerm(ruleLine);
        terms.append(firstTerm);

        # remove parsed initial term
        ruleLine = ruleLine\
            .split(firstTerm.VariableValue)[1][firstTerm.ClosingBracketsCount:]\
            .strip()

        # get result text
        resultText = ruleLine\
            .split(" then ")[1]\
            .strip()

        resultTerm = FclParser.CreateTerm(resultText);
        result = resultTerm;

        # remove result text
        ruleLine = ruleLine\
            .split(" then ")[0]\
            .strip()

        # chained and/or connectives, this is just a hacky way of making sure
        # we split all connectives.
        # this however might break on unknown connectives.
        chainedTerms = ruleLine\
            .replace("and ", "#and# ")\
            .replace("or ", "#or# ")\
            .split("#");

        # safely remove all nones
        chainedTerms = list(filter(None, chainedTerms))

        # add subsequent terms
        for i in range(0, len(chainedTerms), 2):
            connective = chainedTerms[i];
            variable = chainedTerms[i + 1];

            chainedVariableConnectiveText = connective.strip();

            chainedVariableConnectiveEnum = \
                LogicalConnectiveEnum.And if chainedVariableConnectiveText == str(LogicalConnectiveEnum.And) \
                else LogicalConnectiveEnum.Or if chainedVariableConnectiveText == str(LogicalConnectiveEnum.Or) \
                else LogicalConnectiveEnum._None;

            if (chainedVariableConnectiveEnum == LogicalConnectiveEnum._None):
                # something not right, cannot have subsequent terms with
                # None or unknown connectives
                print("Incorrect Logical Connective used for subsequent term - ", chainedVariableConnectiveText);
                continue

            chainedTerm = FclParser.CreateTerm(variable);
            chainedTerm.LogicalConnective = chainedVariableConnectiveEnum;

            terms.append(chainedTerm);

        rule = Rule(name, terms, result);
        return rule;

    def CreateTerm(termText):
        variableName = str();
        variableValue = str();
        variableIsNegated = False;
        variableOpeningBrackets = 0;
        variableClosingBrackets = 0;

        variableName = termText\
            .split("is")[0]\
            .strip()

        if "(" in variableName:
            variableOpeningBrackets = variableName.count("(");
            variableName = variableName.replace("(", str());

        variableValue = termText\
            .split("is")[1]\
            .strip()\
            .split(" ")[0]\
            .strip();

        if "not" in variableValue:
            variableValue =  termText\
                .split("is")[1]\
                .strip()\
                .split(" ")[1]\
                .strip()
            variableIsNegated = True;

        if ")" in variableValue:
            variableClosingBrackets = variableValue.count(")");
            variableValue = variableValue.replace(")", str());

        term = Term(\
            LogicalConnectiveEnum._None,\
            variableIsNegated,\
            variableOpeningBrackets,\
            variableClosingBrackets,\
            variableName,\
            variableValue);

        return term;

    # helper
    def __ReadDataFile(fileName):
        return open("data/" + fileName)\
            .read()\
            .splitlines();

    # validation
    def __CheckRuleLineIsValid(ruleLine):
        if ruleLine.count("(") != ruleLine.count(")"):
            raise Exception("Invalid number of brackets used. Please make sure all brackets are matched.");
            return False;

        return True;