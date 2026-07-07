## Running locally

```shell
OPENAI_API_KEY=your-key uv run uvicorn dnd.server.app:app --port 8000 --reload
```

The API is then available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

## Deployment

Deployment is fully automated via GitHub Actions. Every push to `main`:

1. Builds a Docker image and pushes it to Amazon ECR.
2. Runs `terraform apply` to update the Lambda function to the new image.

Manual deploys can be triggered from the GitHub Actions UI.

A shared **development environment** can be deployed from any branch via the **Deploy Development Environment** workflow (manual trigger only). It is automatically destroyed when a branch is merged to `main`.

### First-time bootstrap

Run once before CI can deploy. The recommended way is via **AWS CloudShell** — it runs in your browser, is already authenticated with your console session, and has the AWS CLI pre-installed. No local credentials needed.

**Step 1 — Open CloudShell and install Terraform**

Open [AWS CloudShell](https://console.aws.amazon.com/cloudshell) (icon in the top navigation bar of the AWS console). Then install Terraform:

```shell
sudo yum install -y yum-utils && \
  sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo && \
  sudo yum install -y terraform
```

**Step 2 — Clone the repo (in CloudShell)**

```shell
git clone https://github.com/Tesla2000/dnd-character-creator.git && \
  cd dnd-character-creator
```

**Step 3 — Create the Terraform state bucket (in CloudShell)**

```shell
aws s3api create-bucket \
    --bucket dnd-character-creator-tf-state \
    --region eu-central-1 \
    --create-bucket-configuration LocationConstraint=eu-central-1 && \
  aws s3api put-bucket-versioning \
    --bucket dnd-character-creator-tf-state \
    --versioning-configuration Status=Enabled
```

**Step 4 — Apply Terraform (in CloudShell)**

```shell
cd terraform && \
  terraform init -backend-config="key=dnd/production/terraform.tfstate" && \
  terraform apply -var="aws_profile=" -var="environment=production"
```

If this fails with `EntityAlreadyExists`, some resources already exist in your account. Import each conflicting resource with `terraform import <resource> <id>` and re-run the apply command until it succeeds.

CloudShell's credentials are used automatically — no profile needed. This provisions all infrastructure (ECR, Lambda, API Gateway, IAM) and grants the CI role the permissions it needs for future deploys.

**Step 5 — Set the OpenAI API key (in CloudShell)**

```shell
aws ssm put-parameter \
  --name /dnd/openai_api_key \
  --value "sk-..." \
  --type SecureString \
  --overwrite
```

**Step 6 — Set the development OpenAI API key (in CloudShell)**

```shell
aws ssm put-parameter --name /dnd/development/openai_api_key --value "sk-..." --type SecureString --overwrite --region eu-central-1
```

**Step 7 — Trigger the first deploy**

Merge the `deployment` branch into `main`. The CI pipeline will run automatically on push, or can be triggered manually from the [GitHub Actions UI](https://github.com/Tesla2000/dnd-character-creator/actions).

After this first production deploy, Terraform will permanently manage both deployer roles and all infrastructure going forward.

---

Alternatively, run locally using a CLI profile. Create an IAM user named `dnd-character-creator`, attach a policy using the contents of [`terraform/bootstrap-policy.json`](terraform/bootstrap-policy.json), generate an access key (**Security credentials → Access keys → CLI**), then:

```shell
aws configure --profile dnd-character-creator
cd terraform && terraform init -backend-config="key=dnd/production/terraform.tfstate"
terraform apply -var="aws_profile=dnd-character-creator" -var="environment=production"
```

## Docker

```shell
docker build -t dnd-character-creator .
```
