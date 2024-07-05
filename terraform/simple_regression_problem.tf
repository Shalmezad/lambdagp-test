locals {
  simple_regression_problem_path_root = "../simple_regression_problem"
  simple_regression_problem_zip_path = "${path.module}/../build/simple_regression_problem.zip"
}

resource "null_resource" "install_simple_regression_problem_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${local.simple_regression_problem_path_root}/requirements.txt -t ${local.simple_regression_problem_path_root}/"
  }
  
  triggers = {
    dependencies_versions = filemd5("${local.simple_regression_problem_path_root}/requirements.txt")
    source_versions = filemd5("${local.simple_regression_problem_path_root}/simple_regression_problem.py")
  }
}

resource "random_uuid" "simple_regression_problem_src_hash" {
  keepers = {
    for filename in setunion(
      fileset(local.simple_regression_problem_path_root, "simple_regression_problem.py"),
      fileset(local.simple_regression_problem_path_root, "requirements.txt")
    ):
      filename => filemd5("${local.simple_regression_problem_path_root}/${filename}")
  }
}

data "archive_file" "simple_regression_problem_zip" {
  depends_on = [null_resource.install_simple_regression_problem_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]
  source_dir  = local.simple_regression_problem_path_root
  type        = "zip"
  output_path = local.simple_regression_problem_zip_path
}

resource "aws_lambda_function" "simple_regression_problem" {
  filename         = local.simple_regression_problem_zip_path
  function_name    = "simple_regression_problem"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "simple_regression_problem.lambda_handler"
  source_code_hash = data.archive_file.simple_regression_problem_zip.output_base64sha256
  runtime          = "python3.8"
}

