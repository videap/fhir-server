# Adapters

The adapters folder will store the code for the Core elements, from Hexagonal Architecture.

Adapters: Do not have business rules, but consume services from the core. It also communicate with Connectors and use Dependency injection, so the connectors are imported as external libraries. It executes data validations, specific data transformation and can should not reuse other adaptors, as they are isolated from each other. To run a function or a process that goes from one adapter to another, the services (core) are needed, as they hold business rules. These elements can be mocked for unit tests but must be used for integration/contracts tests.