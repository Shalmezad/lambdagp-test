module "simple_regression_problem" {
  source = "./modules/python-lambda"
  name = "simple_regression_problem"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}