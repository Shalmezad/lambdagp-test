locals {
  simple_regression_problem_init_zip_path = "${path.module}/../build/simple_regression_problem_init.zip"
  simple_regression_problem_step_zip_path = "${path.module}/../build/simple_regression_problem_step.zip"
}

data "archive_file" "simple_regression_problem_init_zip" {
  type        = "zip"
  source_file = "${path.module}/../simple-regression-problem/handler-init.py"
  output_path = local.simple_regression_problem_init_zip_path
}

data "archive_file" "simple_regression_problem_step_zip" {
  type        = "zip"
  source_file = "${path.module}/../simple-regression-problem/handler-step.py"
  output_path = local.simple_regression_problem_step_zip_path
}

resource "aws_lambda_function" "simple_regression_problem_init" {
  filename         = local.simple_regression_problem_init_zip_path
  function_name    = "simple_regression_problem_init"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "handler-init.init"
  source_code_hash = data.archive_file.simple_regression_problem_init_zip.output_base64sha256
  runtime          = "python3.7"
}

resource "aws_lambda_function" "simple_regression_problem_step" {
  filename         = local.simple_regression_problem_step_zip_path
  function_name    = "simple_regression_problem_step"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "handler-step.step"
  source_code_hash = data.archive_file.simple_regression_problem_step_zip.output_base64sha256
  runtime          = "python3.7"
}