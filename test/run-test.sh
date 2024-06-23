#!/bin/bash

SCRIPT_ROOT=${BASH_SOURCE%/*}

# https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/start-execution.html
awslocal stepfunctions\
    start-execution \
    --region us-west-2 \
    --state-machine-arn arn:aws:states:us-west-2:000000000000:stateMachine:measure-individual \
    --input "$(cat $SCRIPT_ROOT/test-input.json)" \
    > $SCRIPT_ROOT/execution-data.json