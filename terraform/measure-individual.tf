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

resource "aws_sfn_state_machine" "measure_individual" {
  name     = "measure-individual"
  role_arn = aws_iam_role.state_machine_role.arn
  definition = templatefile("${path.module}/measure-individual.asl.json", {
    init_problem_lambda_arn = aws_lambda_function.simple_regression_problem_init.arn,
    gp_executor_lambda_arn = aws_lambda_function.tree_executor.arn,
    step_problem_lambda_arn = aws_lambda_function.simple_regression_problem_step.arn,
  })
}
