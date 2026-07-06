resource "aws_lambda_function" "app" {
  function_name = "dnd-character-creator"
  role          = aws_iam_role.dnd_lambda_exec.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app.repository_url}:${var.image_tag}"

  memory_size = var.lambda_memory_mb
  timeout     = var.lambda_timeout_s

  environment {
    variables = {
      OPENAI_API_KEY = data.aws_ssm_parameter.openai_api_key.value
    }
  }
}
