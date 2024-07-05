module "cgp_builder" {
  source = "./modules/python-lambda"
  name = "cgp_builder"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}