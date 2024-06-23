locals {
  tree_executor_zip_path = "${path.module}/../build/tree_executor.zip"
}

data "archive_file" "tree_executor_zip" {
  type        = "zip"
  source_file = "${path.module}/../tree-executor/handler.py"
  output_path = local.tree_executor_zip_path
}

resource "aws_lambda_function" "tree_executor" {
  filename         = local.tree_executor_zip_path
  function_name    = "tree_executor"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "handler.lambda_handler"
  source_code_hash = data.archive_file.tree_executor_zip.output_base64sha256
  runtime          = "python3.7"
}

