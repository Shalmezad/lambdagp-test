# Make sure to run `localstack start` beforehand

create_replace_lambda() {
    FUNCTION_NAME=$1
    RUNTIME=$2
    ZIP_FILE=$3
    HANDLER=$4

    # Check existance
    awslocal lambda get-function --function-name $FUNCTION_NAME > /dev/null 2>&1
    if [ 0 -eq $? ]; then
        echo "Replacing $FUNCTION_NAME"
        awslocal lambda update-function-code \
            --function-name  $FUNCTION_NAME \
            --zip-file $ZIP_FILE \
            > /dev/null
    else
        echo "Creating $FUNCTION_NAME"
        awslocal lambda create-function \
            --function-name $FUNCTION_NAME \
            --runtime $RUNTIME \
            --zip-file $ZIP_FILE \
            --handler $HANDLER \
            --role arn:aws:iam::000000000000:role/lambda-role \
            > /dev/null
    fi
}

mkdir -p build/
zip -j build/example-handler.zip example-handler/index.js
zip -j build/cgp-executor.zip cgp-executor/handler.py

# create_replace_lambda \
#     example \
#     nodejs18.x \
#     fileb://build/example-handler.zip \
#     index.handler

# # Run a test:
# awslocal lambda invoke --function-name example \
#     --cli-binary-format raw-in-base64-out \
#     --payload '{"body": "{\"num1\": \"10\", \"num2\": \"10\"}" }' \
#     output.txt

create_replace_lambda \
    cgp-executor \
    python3.12 \
    fileb://build/cgp-executor.zip \
    handler.lambda_handler

awslocal lambda invoke --function-name cgp-executor \
    --cli-binary-format raw-in-base64-out \
    --payload '{"body": "{\"num1\": \"10\", \"num2\": \"10\"}" }' \
    output.txt