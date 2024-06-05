## Description
For this evidence, I chose Dart as the base language from which I’m going to extract my grammar.
Dart is a client-optimized programming language developed by Google, it offers a framework for building highly performant applications. By choosing Dart, I hope to improve my understanding of the language and to better exploit its capabilities.


## Models

### Making The Grammar

To simplify the implementation, I'm utilizing a subset of the Dart programming language as the foundation for my grammar. Specifically, I'll focus on crafting a simple grammar for non-anonymous, non-recursive function declarations that will deliberately include ambiguity and left recursion for explanation purposes. The initial structure is adapted from Dart's official documentation (Dart, n.d.).

#### Proposed Grammar:

- **F** -> Identifier (Parameters) Body | Identifier () Body
- **Identifier** -> DataType name | name
- **Parameters** -> Parameters, Parameters | Identifier
- **Body** -> {} | {content} | {ReturnStatement} | {content ReturnStatement}
- **ReturnStatement** -> return value
- **DataType** -> int | double | String | bool

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

The `Parameters` rule still exhibits left recursion, which we need to eliminate to prevent parsing issues. By redefining the production to use right recursion through an intermediate state **P'**, we can convert the recursion to this:
- **Parameters** -> Identifier P'
- **P'** -> , Identifier P' | ε

#### Final Grammar:

With these modifications, our grammar is now free from both ambiguity and left recursion:

- **F** -> Identifier (Parameters) Body | Identifier () Body
- **Identifier** -> DataType name | name
- **Parameters** -> Identifier P'
- **P'** -> , Identifier P' | ε
- **Body** -> {} | {content} | {ReturnStatement} | {content ReturnStatement}
- **ReturnStatement** -> return value
- **DataType** -> int | double | String | bool
