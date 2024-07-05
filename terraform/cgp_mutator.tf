module "cgp_mutator" {
  source = "./modules/python-lambda"
  name = "cgp_mutator"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}