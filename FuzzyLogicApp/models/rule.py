from decimal import Decimal;

from models.term import Term;
from enums.logical_connective_enum import LogicalConnectiveEnum;

class Rule:
    def __str__(self):
        value = "Rule: " + self.Name + "\n"

        for term in self.Terms:
            value += str(term) + "\n";
            continue;

        value += "\t=>" + str(self.Result);

        return value;

    # a bit too lengthy for a constructor
    def __init__(self, ruleLine):
        self.RawRuleLine = str();
        self.Name = str();
        self.Terms = list();
        self.Result = None; # Term type

        self.RawRuleLine = ruleLine.lower();

        self.CheckRuleLineIsValid();

        ruleLine = ruleLine.lower()

        # get rule name
        ruleName = ruleLine\
            .split(":")[0]\
            .strip()

        self.Name = ruleName

        # remove parsed data
        ruleLine = ruleLine\
            .split("if ")[1]\
            .strip()

        firstTerm = self.GetTerm(ruleLine);

        self.Terms\
            .append(firstTerm);

        # remove parsed data
        ruleLine = ruleLine\
            .split(firstTerm.VariableValue)[1][firstTerm.ClosingBracketsCount:]\
            .strip()

        # text to get result from
        resultText = ruleLine\
            .split(" then ")[1]\
            .strip()

        resultTerm = self.GetTerm(resultText);
        self.Result = resultTerm;

        # remove parsed data
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

        # TODO: get rid of empty entries, couldn't figure out a neater way to do it. Definitely hacky
        if "" in chainedTerms:
            chainedTerms.remove("");

        # add subsequent terms
        for i in range(0, len(chainedTerms), 2):
            connective = chainedTerms[i];
            variable = chainedTerms[i+1];

            chainedVariableConnectiveText = connective.strip();

            chainedVariableConnectiveEnum = \
                LogicalConnectiveEnum.And if chainedVariableConnectiveText == str(LogicalConnectiveEnum.And) \
                else LogicalConnectiveEnum.Or if chainedVariableConnectiveText == str(LogicalConnectiveEnum.Or) \
                else LogicalConnectiveEnum._None

            if (chainedVariableConnectiveEnum == LogicalConnectiveEnum._None):
                # something not right, cannot have subsequent terms with
                # None or unknown connectives
                print("Incorrect Logical Connective used for subsequent term - ", chainedVariableConnectiveText)
                continue

            chainedTerm = self.GetTerm(variable);
            chainedTerm.LogicalConnective = chainedVariableConnectiveEnum;

            self.Terms.append(chainedTerm);
        return;

    def GetTerm(self, ruleText):
        variableName = str();
        variableValue = str();
        variableIsNegated = False;
        variableOpeningBrackets = 0;
        variableClosingBrackets = 0;

        variableName = ruleText\
            .split("is")[0]\
            .strip()

        if "(" in variableName:
            variableOpeningBrackets = variableName.count("(");
            variableName = variableName.replace("(", str());

        variableValue = ruleText\
            .split("is")[1]\
            .strip()\
            .split(" ")[0]\
            .strip()

        if "not" in variableValue:
            variableValue =  ruleText\
                .split("is")[1]\
                .strip()\
                .split(" ")[1]\
                .strip()
            variableIsNegated = True;

        if ")" in variableValue:
            variableClosingBrackets = variableValue.count(")");
            variableValue = variableValue.replace(")", str());

        return Term(\
            LogicalConnectiveEnum._None,\
            variableIsNegated,\
            variableOpeningBrackets,\
            variableClosingBrackets,\
            variableName,\
            variableValue);

    def CheckRuleLineIsValid(self):
        if self.RawRuleLine.count("(") != self.RawRuleLine.count(")"):
            raise Exception("Invalid number of brackets used. Please make sure all brackets are matched.");

        return;