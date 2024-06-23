locals {
  tree_executor_path_root = "../tree-executor"
  tree_executor_zip_path = "${path.module}/../build/tree_executor.zip"
}

resource "null_resource" "install_tree_executor_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${local.tree_executor_path_root}/requirements.txt -t ${local.tree_executor_path_root}/"
  }
  
  triggers = {
    dependencies_versions = filemd5("${local.tree_executor_path_root}/requirements.txt")
    source_versions = filemd5("${local.tree_executor_path_root}/handler.py")
  }
}

resource "random_uuid" "lambda_src_hash" {
  keepers = {
    for filename in setunion(
      fileset(local.tree_executor_path_root, "handler.py"),
      fileset(local.tree_executor_path_root, "requirements.txt")
    ):
      filename => filemd5("${local.tree_executor_path_root}/${filename}")
  }
}

data "archive_file" "tree_executor_zip" {
  depends_on = [null_resource.install_tree_executor_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]
  source_dir  = local.tree_executor_path_root
  type        = "zip"
  output_path = local.tree_executor_zip_path
}

resource "aws_lambda_function" "tree_executor" {
  filename         = local.tree_executor_zip_path
  function_name    = "tree_executor"
  role             = aws_iam_role.iam_for_lambda_tf.arn
  handler          = "handler.lambda_handler"
  source_code_hash = data.archive_file.tree_executor_zip.output_base64sha256
  runtime          = "python3.7"
}

