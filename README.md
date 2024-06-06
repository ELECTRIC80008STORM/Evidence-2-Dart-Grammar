## Description
For this evidence, I chose Dart as the base language from which I’m going to extract my grammar.
Dart is a client-optimized programming language developed by Google, it offers a framework for building highly performant applications. By choosing Dart, I hope to improve my understanding of the language and to better exploit its capabilities.


## Models

### Making The Grammar

To simplify the implementation, I'm utilizing a subset of the Dart programming language as the foundation for my grammar. Specifically, I'll focus on crafting a simple grammar for non-anonymous, non-recursive function declarations that will deliberately include ambiguity and left recursion for explanation purposes. Only declarations for non local functions with a non void return type are going to be accounted for. The initial structure is adapted from Dart's official documentation (Dart, n.d.).

#### Proposed Grammar:

- **F** -> Identifier (Parameters) Body | Identifier () Body
- **Identifier** -> DataType name | name
- **Parameters** -> Parameters, Parameters | Identifier
- **Body** -> {} | {content} | {ReturnStatement} | {content ReturnStatement}
- **ReturnStatement** -> return value
- **DataType** -> int | double | String | bool | void

### Eliminating Ambiguity and Left Recursion

With the grammar established, we’ll now focus on making it deterministic to make it easier to use common parsers like NLTK. For this, eliminating both ambiguity and left recursion is needed.

#### Ambiguity in Parameters:

The ambiguity in our grammar originates from the `Parameters` production:
- **Parameters** -> Parameters, Parameters | Identifier

This rule introduces ambiguity, as it allows expressions like `int x, i, String string` to be grouped in multiple ways, leading to different interpretations and Abstract Syntax Trees for the same input string. For example:
- Grouping 1: int x, (i, String string) -> Parameters, (Parameters, T)
- Grouping 2: (int x, i), String string -> (Parameters, T), T

To resolve this, we can introduce an auxiliary non-terminal, **T**, to differentiate groupings clearly:
- **Parameters** -> Parameters, T | T
- **T** -> Identifier

Simplifying further, we refine it to:
- **Parameters** -> Parameters, Identifier | Identifier

#### Resolving Left Recursion:

The `Parameters` rule still exhibits left recursion, which we need to eliminate to prevent parsing issues. By redefining the production to use right recursion through an intermediate state **P**, we can convert the recursion to this:
- **Parameters** -> Identifier P
- **P** -> , Identifier P | ε

Now that we know how to resolve both problems for the `Parameters` production, we can apply the same process to `F` and `Body` productions, the only places where ambiguity or left recursion is left. The result productions would look as follows:

#### Ambiguity in F:
- **F** -> Identifier (ParametersList) Body
- **ParametersList** -> Parameters |  ε

#### Ambiguity in Body:
- **Body** -> {BodyContent}
- **BodyContent** -> ε | content | ReturnStatement | content ReturnStatement

#### Resolving Left Recursion in Body:
- **Body** -> {BodyContent}
- **BodyContent** -> ε | content B’ | ReturnStatement
- **B'** -> ReturnStatement | ε

#### Final Grammar:
With these modifications, our grammar is now free from both ambiguity and left recursion:
- **F** -> Identifier ( ParametersList ) Body
- **Identifier** -> DataType name | name
- **ParametersList** -> Parameters | ε
- **Parameters** -> Identifier P
- **P** -> , Identifier P | ε
- **Body** -> { BodyContent }
- **BodyContent** -> ε | content B | ReturnStatement
- **B** -> ReturnStatement | ε
- **ReturnStatement** -> return value
- **DataType** -> int | double | String | bool


## Implementation

The implementation involves utilizing the grammar to check the given strings against it, with this we effectively determine if they could form part of the language. The implementation can be found in the `dartCFGTester.py` file. Given that it’s easy to make mistakes when giving input to the function, the user will only be able to run the code and see the tests and their results for the example strings. Those same tests will be commented in here with their respective LL1 parsing AST. For the implementation to work, the NLTK module is needed.

This module is used for making it easy to define the Context-Free Grammar (CFG) and for creating the parser and using it:
- It can be installed on Ubuntu with the following command:
  ```bash
  $ sudo apt install python3-nltk
  ```
- Here is a guide to install it on other operating systems: [Guide](https://www.nltk.org/install.html)


## Tests

The `dartCFGTester.py` file contains all of the test cases. As explained before, in this section we are going to put the tests with their given Abstract Syntax Trees, although the invalid strings won’t always have an AST, or at least not a complete one. To obtain the AST, we are going to use the LL(1) Parser Visualization tool from Princeton (Kincaid Z. and Zhu S., n.d.).

### Valid Strings

- **String**: `int name ( int name ) { return value }`
  ![AST for int name ( int name ) { return value }](PicturesFromTests/ValidTest1.png)

- **String**: `int name ( ) { content return value }`
  ![AST for int name ( ) { content return value }](PicturesFromTests/ValidTest2.png)

- **String**: `double name ( ) { content return value }`
  ![AST for double name ( ) { content return value }](PicturesFromTests/ValidTest3.png)

- **String**: `String name ( int name , double name ) { return value }`
  ![AST for String name ( int name , double name ) { return value }](PicturesFromTests/ValidTest4.png)

- **String**: `bool name ( String name ) { return value }`
  ![AST for bool name ( String name ) { return value }](PicturesFromTests/ValidTest5.png)


### Invalid Strings

- **String**: `( int name ) { }`
  **Description**: The function name is missing.
  ![AST for ( int name ) { }](PicturesFromTests/InvalidTest1.png)

- **String**: `name { content return value }`
  **Description**: The parentheses for parameters are missing.
  ![AST for name { content return value }](PicturesFromTests/InvalidTest2.png)

- **String**: `int name ( int name ) { int name ( String char ) { } }`
  **Description**: Local functions declarations are not supported by the proposed grammar as detailed above.
  ![AST for int name ( int name ) { int name ( String char ) { } }](PicturesFromTests/InvalidTest3.png)

- **String**: `name ( int name ) { return }{}`
  **Description**: The “value” to be returned is missing.
  ![AST for name ( int name ) { return }{}](PicturesFromTests/InvalidTest4.png)

- **String**: `int name ( int name ) content return value`
  **Description**: The curly brackets of the function body are missing.
  ![AST for int name ( int name ) content return value](PicturesFromTests/InvalidTest5.png)

- **String**: `double name ( String name , int name )`
  **Description**: The body as a whole is missing.
  ![AST for double name ( String name , int name )](PicturesFromTests/InvalidTest6.png)

