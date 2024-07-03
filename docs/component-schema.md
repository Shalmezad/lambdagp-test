# Component Schema

This doc describes the inputs/outputs of a component

## Component key

Every component should have a unique key that it can use to access the main data dictionaries

## Handler

Every component should define `lambda_handler` as it's main function

## Metadata

Every event in/out of a component will have a `metadata` dictionary.
This dictionary is meant for temporary information that should be kept between invocations.
For example, 
    a `GenerationRunner` component may keep track of what generation it's on,
    a `IndividualGrader` component may keep track of current cases it's tested so it knows which ones still remain,

Example:
```
event: {
    "metadata": {
        "foo": ...
        "bar": ...
    }
}
```

A component *MUST* copy this metadata from it's input to it's output.

A component *MAY* modify this metadata for it's own component key only.

A component *MUST NOT* modify any other component key

A component *MUST* clear out it's own metadata when it's no longer needed (otherwise it'll waste payload space)

## Config

Every event in/out of a component will have a `config` dictionary.
This dictionary is meant for global run values (mutation rates, population sizes, etc)

Example:
```
event: {
    "config": {
        "foo": ...
        "bar": ...
    }
}
```

A component *MUST* copy this metadata from it's input to it's output.

A component *MUST NOT* modify this dictionary


## Keys and types

Keys throughout will be `snake_case`

These keys are used in a number of different components:

* `individuals` / `population` / `children` - These will be dictionaries, where the key is a globally unique id (such as version 4 UUIDs) for that individual, and the value will be the genotype of the individual. Anything that creates a new individual (be it a brand new one or a variation of existing) should create a new unique id for that individual.
* `cases` - This will be a dictionary, where key is the case id (relevant to the problem). The value will be an array of values (either inputs or outputs depending on where it's used). The problem is responsible for maintaining it's metadata to keep track of ids and what they represent (problem inputs, world state, etc)
* `fitnesses` - This will be a dictionary, where key is an individual id, and values are another dictionary. The value dictionary keys are case_id, and values are fitness measurements.

### Fitnesses example

```json
{
    "fitnesses": {
        "individual_f": {
            "case_1": 3.14,
            "case_2": 42,
        },
        "individual_g": {
            "case_1": 7,
            "case_2": 9999.9
        }
    }
}
```