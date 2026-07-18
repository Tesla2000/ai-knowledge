#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TF_DIR="$ROOT_DIR/terraform"

echo "==> terraform init"
terraform -chdir="$TF_DIR" init

echo "==> creating ECR repository"
terraform -chdir="$TF_DIR" apply -target=aws_ecr_repository.app -auto-approve

ECR_URL=$(terraform -chdir="$TF_DIR" output -raw ecr_repository_url)
AWS_REGION=$(terraform -chdir="$TF_DIR" output -json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin)" 2>/dev/null || true)
# Derive region from ECR URL (format: <account>.dkr.ecr.<region>.amazonaws.com/<name>)
REGION=$(echo "$ECR_URL" | sed 's/.*ecr\.\([^.]*\)\..*/\1/')

echo "==> docker login to ECR ($ECR_URL)"
aws ecr get-login-password --region "$REGION" --profile dnd-character-creator \
  | docker login --username AWS --password-stdin "$ECR_URL"

echo "==> docker login to public ECR (for base image)"
aws ecr-public get-login-password --region us-east-1 --profile dnd-character-creator \
  | docker login --username AWS --password-stdin public.ecr.aws

echo "==> docker build"
docker build -t "$ECR_URL:latest" "$ROOT_DIR"

echo "==> docker push"
docker push "$ECR_URL:latest"

echo "==> terraform apply (full)"
terraform -chdir="$TF_DIR" apply -auto-approve

echo ""
echo "Deployed. API URL:"
terraform -chdir="$TF_DIR" output -raw api_url
echo ""
