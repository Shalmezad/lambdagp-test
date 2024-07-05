module "simple_population_builder" {
  source = "./modules/python-lambda"
  name = "simple_population_builder"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}