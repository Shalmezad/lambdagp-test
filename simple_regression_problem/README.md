# Simple Regression Problem

This is an `Individual Measurer` component.

Based off the example run on page 135 of "Genetic Programming An Introduction" by Wolfgang Banzhaf et al,
which is the function x^2 / 2 for the input range [0.0, 1.0) with a step size of 0.1

For fitness, this does an absolute error measurement between the actual and expected values.

As this only has 10 fitness cases, this does not do multiple calls to the `Individual Executor` component.