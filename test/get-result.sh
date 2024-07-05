#!/bin/bash


SCRIPT_ROOT=${BASH_SOURCE%/*}

ARN=$(cat $SCRIPT_ROOT/execution-data.json| jq -r .executionArn)
awslocal stepfunctions \
    describe-execution \
    --execution-arn $ARN \
    --region us-west-2

awslocal stepfunctions \
    get-execution-history \
    --execution-arn $ARN \
    --region us-west-2