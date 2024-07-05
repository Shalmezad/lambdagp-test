module "rmse_tournament_selector" {
  source = "./modules/python-lambda"
  name = "rmse_tournament_selector"
  iam_arn = aws_iam_role.iam_for_lambda_tf.arn
}