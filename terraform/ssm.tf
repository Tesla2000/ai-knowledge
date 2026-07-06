# Placeholder — populate the real value before running the full apply:
#   aws ssm put-parameter \
#     --name /dnd/openai_api_key \
#     --value "sk-..." \
#     --type SecureString \
#     --overwrite
resource "aws_ssm_parameter" "openai_api_key" {
  name      = "/dnd/openai_api_key"
  type      = "SecureString"
  value     = "REPLACE_ME"
  overwrite = true

  lifecycle {
    ignore_changes = [value]
  }
}

data "aws_ssm_parameter" "openai_api_key" {
  name            = aws_ssm_parameter.openai_api_key.name
  with_decryption = true
}
