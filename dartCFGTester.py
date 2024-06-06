"""
Function Declaration Grammar for Dart - Context-Free Grammar (CFG)

This script defines a (representative and simplify) CFG for Dart function declarations and
uses a recursive descent parser to evaluate if entire statements are syntactically correct
according to the grammar rules. This ensures that the inputs conform to the expected format
of Dart function declarations.
"""

from nltk import CFG
from nltk.parse import ChartParser
import time

# Define the grammar for Dart function declarations
# using Context-Free Grammar (CFG).
grammar = CFG.fromstring("""
  F -> Identifier '(' ParametersList ')' Body
  Identifier -> DataType 'name' | 'name'
  ParametersList -> Parameters | 
  Parameters -> Identifier P
  P -> ',' Identifier P | 
  Body -> '{' BodyContent '}'
  BodyContent -> 'content' B | ReturnStatement | 
  B -> ReturnStatement | 
  ReturnStatement -> 'return' 'value'
  DataType -> 'int' | 'double' | 'String' | 'bool'
""")

# Initialize the parser with the defined grammar.
parser = ChartParser(grammar)

def isSyntacticallyCorrect(testedString):
    """
    Check if the tested string is syntactically correct according to the defined CFG.

    Parameters:
    testedString (str): The string to be tested against the CFG.

    Returns:
    bool: True if the string is syntactically correct, False otherwise.
    """

    try:
        tokens = testedString.split()
        syntaxTree = ''
        for x in parser.parse(tokens):
            syntaxTree = str(x)
        return bool(syntaxTree)
    except Exception:
        return False

# List of valid test strings to check the grammar.
validTests = [
    "int name ( int name ) { return value }",
    "int name ( ) { content return value }",
    "double name ( ) { content return value }",
    "String name ( int name , double name ) { return value }",
    "bool name ( String name ) { return value }",
]

# List of invalid test strings to check the grammar.
invalidTests = [
    "( int name ) { }",
    "name { content return value }",
    "int name ( int name ) { int name ( String char ) { } }",
    "name ( int name ) { return }{}",
    "int name ( int name ) content return value",
    "double name ( String name , int name )",
]

# Execute and print results for valid and invalid test cases.
print("Tests With Valid Input")
for i, test in enumerate(validTests, start = 1):
    result = isSyntacticallyCorrect(test)
    print(f"Test {i}\nString: {test}\n")
    if result:
        print('The string is valid as it should!!!')
    else:
        print('The string is invalid, something went wrong with the parser!!!')
    time.sleep(3)
    print("\n")

print("Tests With Invalid Input")
for i, test in enumerate(invalidTests, start = 1):
    result = isSyntacticallyCorrect(test)
    print(f"Test {i}\nString: {test}\n")
    if not result:
        print('The string is invalid as it should!!!')
    else:
        print('The string is valid, something went wrong with the parser!!!')
    time.sleep(3)
    print("\n")
