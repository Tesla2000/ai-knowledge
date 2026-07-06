variable "aws_profile" {
  description = "AWS CLI profile to use (empty string uses environment credentials)"
  type        = string
  default     = ""
}

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-central-1"
}

variable "lambda_memory_mb" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout_s" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "github_repo" {
  description = "GitHub repo in owner/name format (for OIDC trust policy)"
  type        = string
  default     = "Tesla2000/dnd-character-creator"
}
