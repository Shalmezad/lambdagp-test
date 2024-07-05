module "cgp_executor" {
  source = "./modules/python-lambda"
  name = "cgp_executor"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}