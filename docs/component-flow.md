# Component Flow

This doc describes a high level overview of components, and how they should flow

## Population Builder

This component is responsible for building the initial population

This component is called from:
* `Nothing` - This is the very first component called in a run
* `Individual Builder` - Takes the individual[s] returned from this component, and adds them to the population

It returns 1 of two results:

* `is_done: True`
    * Population has been built, and will be present in the key `population`
    * This should then move on to `Generation Runner`
* `is_done: False`
    * Population needs more individuals
    * From here, `Individual Builder` is called

## Individual Builder

This component is responsible for building a single brand new individual

This component is called from:
* `Population Builder` - Calls this when more individuals are needed for the initial population

It returns:
* `individuals`
    * This is the typical `"individual_id": <some_data>` that is used for populations
    * This component may return more than one individual at a time

Results from this component go immediately back to the population builder

## Generation Runner

This component decides whether to run a generation or not. 

This can be based on any sort of criteria (fitness requirements met, cap number of generations, etc)

This component is called from:
* `Population Builder` - Means this is the first generation run
* `Generation Builder` - Means we have a brand new set of individuals

It returns 1 of two results:
* `is_done: True`
    * We are done running
    * This should end a run (barring any additional recording steps)
* `is_done: False`
    * We should run this generation
    * Will have the `population` that was passed to this component
    * From here, `Generation Measurer` is called

## Generation Measurer

This component is responsible managing the fitness measurement of an entire generation. 

It returns 1 of two results:
* `is_done: True`
    * The entire generation has been graded
    * This will have both `population`, and `fitnesses`
    * From here, `Generation Builder` is called
* `is_done: False`
    * Generation is missing some measurements
    * This will have `individuals` to measure
    * From here, `Individual Measurer` is called

## Individual Measurer

This component is the actual "problem", and is responsible for measuring the fitness of the individual[s] passed

It returns one of two results:
* `is_done: True`
    * The individuals have been measured
    * Will return `fitnesses` for the individuals measured
    * From here, `Generation Measurer` is called
* `is_done: False`
    * Some subset of the individuals we're measuring still need measured
    * Will return `cases` and `individuals`
    * From here, `Individual Executor` is called

## Individual Executor

This component is responsible for executing an individual on given input.

This receives `cases` and `individuals` from Individual Measurer

This returns `case_results` which is a dictionary. Keys are `individual_ids`. Values are dictionaries. These value dictionaries have `case_id` keys and case output values

## Generation Builder

This component is responsible for managing the building of a new generation.

This will receive 1 of two values:
* `fitnesses` / `populations`
    * Sent from `Generation Measurer`
    * These should be saved in metadata and passed to `Generation Runner`
* `children`
    * Sent from `Child Builder`
    * Should be appended to the new population

This returns 1 of two results:
* `is_done: True`
    * Generation has been built
    * Will have `population` as the new population
    * From here, `Generation Runner` is called to run on the new population (if execution should continue)
* `is_done: False`
    * We do not have enough individuals for the new population
    * From here, the `population` and `fitnesses` are send to `Child Builder`

## Child Builder

This component is responsible for building children

This returns 1 of two results:
* `is_done: True`
    * Children have been built and will be in `children`
    * May go to either additional transofmrers, or `Generation Builder`
* `is_done: False`
    * We need more individuals selected to make children
    * Has `population` / `fitnesses`
    * Goes to `Parent Selector`

## Parent Selector

This component is responsible for selecting parent[s] from the given population/fitnesses.

