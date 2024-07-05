locals {
  lambda_gp_root = "${path.module}/../../.."
  path_root = "${local.lambda_gp_root}/${var.name}"
  zip_path = "${local.lambda_gp_root}/build/${var.name}.zip"
}

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${local.path_root}/requirements.txt -t ${local.path_root}/"
  }
  
  triggers = {
    dependencies_versions = filemd5("${local.path_root}/requirements.txt")
    source_versions = filemd5("${local.path_root}/${var.name}.py")
  }
}

resource "random_uuid" "src_hash" {
  keepers = {
    for filename in setunion(
      fileset(local.path_root, "${var.name}.py"),
      fileset(local.path_root, "requirements.txt")
    ):
      filename => filemd5("${local.path_root}/${filename}")
  }
}

data "archive_file" "lambda_zip" {
  depends_on = [null_resource.install_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]
  source_dir  = local.path_root
  type        = "zip"
  output_path = local.zip_path
}

resource "aws_lambda_function" "python_lambda" {
  filename         = local.zip_path
  function_name    = var.name
  role             = var.iam_arn
  handler          = "${var.name}.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.10"
}

