data "aws_caller_identity" "current" {}

resource "aws_iam_openid_connect_provider" "github" {
  count           = var.environment == "production" ? 1 : 0
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]  # pragma: allowlist secret

  lifecycle {
    prevent_destroy = true
  }
}

locals {
  oidc_arn = var.environment == "production" ? aws_iam_openid_connect_provider.github[0].arn : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
}

# Production deployer: main branch only
data "aws_iam_policy_document" "production_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [local.oidc_arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:ref:refs/heads/main"]
    }
  }
}

# Development deployer: any branch
data "aws_iam_policy_document" "development_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [local.oidc_arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:ref:refs/heads/*"]
    }
  }
}

resource "aws_iam_role" "dnd_deployer_production" {
  count              = var.environment == "production" ? 1 : 0
  name               = "dnd-deployer-production"
  assume_role_policy = data.aws_iam_policy_document.production_trust.json
}

resource "aws_iam_role" "dnd_deployer_development" {
  count              = var.environment == "production" ? 1 : 0
  name               = "dnd-deployer-development"
  assume_role_policy = data.aws_iam_policy_document.development_trust.json
}

data "aws_iam_policy_document" "deployer_production_policy" {
  statement {
    sid       = "ECRAuth"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    sid = "ECRPushManage"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:CreateRepository",
      "ecr:DeleteRepository",
      "ecr:DescribeRepositories",
      "ecr:SetRepositoryPolicy",
      "ecr:GetRepositoryPolicy",
      "ecr:DeleteRepositoryPolicy",
      "ecr:ListTagsForResource",
      "ecr:TagResource",
      "ecr:UntagResource",
    ]
    resources = ["arn:aws:ecr:${var.aws_region}:${data.aws_caller_identity.current.account_id}:repository/dnd-character-creator"]
  }

  statement {
    sid = "LambdaManage"
    actions = [
      "lambda:CreateFunction",
      "lambda:DeleteFunction",
      "lambda:GetFunction",
      "lambda:UpdateFunctionCode",
      "lambda:UpdateFunctionConfiguration",
      "lambda:AddPermission",
      "lambda:RemovePermission",
      "lambda:GetPolicy",
      "lambda:ListVersionsByFunction",
    ]
    resources = ["arn:aws:lambda:${var.aws_region}:${data.aws_caller_identity.current.account_id}:function:dnd-character-creator"]
  }

  statement {
    sid       = "IAMPassRole"
    actions   = ["iam:PassRole"]
    resources = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dnd-character-creator-exec"]
  }

  statement {
    sid = "IAMManage"
    actions = [
      "iam:CreateRole",
      "iam:DeleteRole",
      "iam:GetRole",
      "iam:UpdateRole",
      "iam:AttachRolePolicy",
      "iam:DetachRolePolicy",
      "iam:PutRolePolicy",
      "iam:GetRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:ListAttachedRolePolicies",
      "iam:ListRolePolicies",
      "iam:ListInstanceProfilesForRole",
      "iam:CreateOpenIDConnectProvider",
      "iam:GetOpenIDConnectProvider",
      "iam:DeleteOpenIDConnectProvider",
      "iam:TagOpenIDConnectProvider",
      "iam:UpdateOpenIDConnectProviderThumbprint",
    ]
    resources = ["*"]
  }

  statement {
    sid       = "APIGatewayManage"
    actions   = ["apigateway:*"]
    resources = ["arn:aws:apigateway:${var.aws_region}::*"]
  }

  statement {
    sid = "SSMManage"
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:PutParameter",
      "ssm:DeleteParameter",
      "ssm:AddTagsToResource",
      "ssm:ListTagsForResource",
    ]
    resources = ["arn:aws:ssm:${var.aws_region}:*:parameter/dnd/openai_api_key"]
  }

  statement {
    sid       = "SSMDescribe"
    actions   = ["ssm:DescribeParameters"]
    resources = ["*"]
  }

  statement {
    sid = "S3State"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket",
      "s3:GetBucketVersioning",
    ]
    resources = [
      "arn:aws:s3:::dnd-character-creator-tf-state",
      "arn:aws:s3:::dnd-character-creator-tf-state/*",
    ]
  }
}

data "aws_iam_policy_document" "deployer_development_policy" {
  statement {
    sid       = "ECRAuth"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    sid = "ECRPushManage"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:CreateRepository",
      "ecr:DeleteRepository",
      "ecr:DescribeRepositories",
      "ecr:SetRepositoryPolicy",
      "ecr:GetRepositoryPolicy",
      "ecr:DeleteRepositoryPolicy",
      "ecr:ListTagsForResource",
      "ecr:TagResource",
      "ecr:UntagResource",
    ]
    resources = ["arn:aws:ecr:${var.aws_region}:${data.aws_caller_identity.current.account_id}:repository/dnd-character-creator-development"]
  }

  statement {
    sid = "LambdaManage"
    actions = [
      "lambda:CreateFunction",
      "lambda:DeleteFunction",
      "lambda:GetFunction",
      "lambda:UpdateFunctionCode",
      "lambda:UpdateFunctionConfiguration",
      "lambda:AddPermission",
      "lambda:RemovePermission",
      "lambda:GetPolicy",
    ]
    resources = ["arn:aws:lambda:${var.aws_region}:${data.aws_caller_identity.current.account_id}:function:dnd-character-creator-development"]
  }

  statement {
    sid       = "LambdaList"
    actions   = ["lambda:ListVersionsByFunction"]
    resources = ["arn:aws:lambda:${var.aws_region}:${data.aws_caller_identity.current.account_id}:function:dnd-character-creator-development*"]
  }

  statement {
    sid       = "IAMPassRole"
    actions   = ["iam:PassRole"]
    resources = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dnd-character-creator-development-exec"]
  }

  statement {
    sid = "IAMManage"
    actions = [
      "iam:CreateRole",
      "iam:DeleteRole",
      "iam:GetRole",
      "iam:UpdateRole",
      "iam:AttachRolePolicy",
      "iam:DetachRolePolicy",
      "iam:PutRolePolicy",
      "iam:GetRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:ListAttachedRolePolicies",
      "iam:ListRolePolicies",
      "iam:ListInstanceProfilesForRole",
    ]
    resources = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dnd-character-creator-development-exec"]
  }

  statement {
    sid       = "APIGatewayManage"
    actions   = ["apigateway:*"]
    resources = ["arn:aws:apigateway:${var.aws_region}::*"]
  }

  statement {
    sid = "SSMManage"
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:PutParameter",
      "ssm:DeleteParameter",
      "ssm:AddTagsToResource",
      "ssm:ListTagsForResource",
    ]
    resources = ["arn:aws:ssm:${var.aws_region}:*:parameter/dnd/development/openai_api_key"]
  }

  statement {
    sid       = "SSMDescribe"
    actions   = ["ssm:DescribeParameters"]
    resources = ["*"]
  }

  statement {
    sid = "S3State"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket",
      "s3:GetBucketVersioning",
    ]
    resources = [
      "arn:aws:s3:::dnd-character-creator-tf-state",
      "arn:aws:s3:::dnd-character-creator-tf-state/*",
    ]
  }
}

resource "aws_iam_role_policy" "dnd_deployer_production" {
  count  = var.environment == "production" ? 1 : 0
  name   = "dnd-deployer-production-policy"
  role   = aws_iam_role.dnd_deployer_production[0].id
  policy = data.aws_iam_policy_document.deployer_production_policy.json
}

resource "aws_iam_role_policy" "dnd_deployer_development" {
  count  = var.environment == "production" ? 1 : 0
  name   = "dnd-deployer-development-policy"
  role   = aws_iam_role.dnd_deployer_development[0].id
  policy = data.aws_iam_policy_document.deployer_development_policy.json
}
