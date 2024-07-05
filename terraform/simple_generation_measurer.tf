module "simple_generation_measurer" {
  source = "./modules/python-lambda"
  name = "simple_generation_measurer"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}