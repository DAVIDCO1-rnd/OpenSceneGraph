from pypeg2 import *
import re


# Define a grammar for a type name
class Type(str):
    grammar = re.compile(r'\b(int|double|float|char|short|long)\b')


# Define a grammar for a variable declaration
class VariableDeclaration(str):
    grammar = Type, name(), ";"


# Define a grammar for a function argument
class Argument(str):
    grammar = Type, name()


# Define a grammar for a function declaration
class FunctionDeclaration(str):
    grammar = Type, name(), "(", optional(csl(Argument)), ")", ";"


# Define a grammar for a C++ program
class Program(List):
    grammar = maybe_some([VariableDeclaration, FunctionDeclaration])


# Example C++ program
source = """
    int x;
    double y;

    int add(int a, int b);
"""

# Parse the program
program = parse(source, Program)

# Print the parsed program
print(program)