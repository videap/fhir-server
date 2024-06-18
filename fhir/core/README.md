# Services

The service folder will store the code for the Core elements, from Hexagonal Architecture.

Core: Only business logic, and has all data required coming as inputs. Inputs and outputs are primitives. It should only have pure functions and should be only accessed by adapters. Extensively tested by unit tests.