
resource "aws_iam_role" "state_machine_role" {
  name = "lambda-gp-state-machine-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_sfn_state_machine" "simple_gp_run" {
  name     = "simple_gp_run"
  role_arn = aws_iam_role.state_machine_role.arn
  definition = templatefile("${path.module}/simple_gp_run.asl.json", {
    population_builder_lambda_arn = module.simple_population_builder.lambda_arn
    generation_runner_lambda_arn = module.simple_generation_runner.lambda_arn
    generation_measurer_lambda_arn = module.simple_generation_measurer.lambda_arn
    generation_builder_lambda_arn = module.simple_generation_builder.lambda_arn
    child_builder_lambda_arn = module.cgp_mutator.lambda_arn
    individual_selector_lambda_arn = module.rmse_tournament_selector.lambda_arn
    individual_measurer_lambda_arn = module.simple_regression_problem.lambda_arn
    individual_executor_lambda_arn = module.cgp_executor.lambda_arn
    individual_builder_lambda_arn = module.cgp_builder.lambda_arn
  })
}