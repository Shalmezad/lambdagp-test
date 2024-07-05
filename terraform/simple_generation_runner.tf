module "simple_generation_runner" {
  source = "./modules/python-lambda"
  name = "simple_generation_runner"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}