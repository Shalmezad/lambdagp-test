locals {
  treeexecutor_path_root = "../treeexecutor"
  treeexecutor_zip_path = "${path.module}/../build/treeexecutor.zip"
}

resource "null_resource" "install_treeexecutor_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${local.treeexecutor_path_root}/requirements.txt -t ${local.treeexecutor_path_root}/"
  }
  
  triggers = {
    dependencies_versions = filemd5("${local.treeexecutor_path_root}/requirements.txt")
    source_versions = filemd5("${local.treeexecutor_path_root}/treexecutor.py")
  }
}

resource "random_uuid" "lambda_src_hash" {
  keepers = {
    for filename in setunion(
      fileset(local.treeexecutor_path_root, "treexecutor.py"),
      fileset(local.treeexecutor_path_root, "requirements.txt")
    ):
      filename => filemd5("${local.treeexecutor_path_root}/${filename}")
  }
}

data "archive_file" "treeexecutor_zip" {
  depends_on = [null_resource.install_treeexecutor_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]
  source_dir  = local.treeexecutor_path_root
  type        = "zip"
  output_path = local.treeexecutor_zip_path
}

resource "aws_lambda_function" "treeexecutor" {
  filename         = local.treeexecutor_zip_path
  function_name    = "treeexecutor"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "treexecutor.lambda_handler"
  source_code_hash = data.archive_file.treeexecutor_zip.output_base64sha256
  runtime          = "python3.8"
}

