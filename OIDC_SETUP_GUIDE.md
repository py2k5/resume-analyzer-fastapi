# GitHub Actions OIDC Setup Guide

## Overview
This guide explains how to set up GitHub Actions with AWS OIDC (OpenID Connect) for secure, keyless authentication to AWS services.

## What is OIDC?
OIDC allows GitHub Actions to assume AWS IAM roles without storing long-term AWS access keys as secrets. This is more secure and follows AWS security best practices.

## Prerequisites
- AWS Account (Account ID: 314146297130)
- GitHub Repository
- AWS CLI access to configure IAM

## Step 1: Configure GitHub OIDC Provider in AWS

### 1.1 Create OIDC Identity Provider
```bash
# Create OIDC identity provider for GitHub
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

### 1.2 Verify OIDC Provider
```bash
# List OIDC providers to verify
aws iam list-open-id-connect-providers
```

## Step 2: Configure IAM Role Trust Policy

### 2.1 Update Trust Policy for OIDC Role
The role `OIDCRole_iamadmin_general` should have a trust policy like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::314146297130:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:your-username/your-repo:*"
        }
      }
    }
  ]
}
```

### 2.2 Update Trust Policy (if needed)
```bash
# Update trust policy for the OIDC role
aws iam update-assume-role-policy \
  --role-name OIDCRole_iamadmin_general \
  --policy-document file://trust-policy.json
```

## Step 3: Required IAM Permissions

### 3.1 Lambda Permissions
The OIDC role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:GetFunction",
        "lambda:AddPermission",
        "lambda:RemovePermission",
        "lambda:ListFunctions"
      ],
      "Resource": "arn:aws:lambda:*:314146297130:function:resume-analyzer*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::314146297130:role/LambdaExecutionRole"
    }
  ]
}
```

### 3.2 API Gateway Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "apigateway:GET",
        "apigateway:POST",
        "apigateway:PUT",
        "apigateway:DELETE",
        "apigateway:PATCH"
      ],
      "Resource": "*"
    }
  ]
}
```

### 3.3 Textract Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "textract:DetectDocumentText",
        "textract:AnalyzeDocument",
        "textract:StartDocumentAnalysis",
        "textract:GetDocumentAnalysis",
        "textract:ListDocumentAnalysisJobs"
      ],
      "Resource": "*"
    }
  ]
}
```

## Step 4: Create Lambda Execution Role

### 4.1 Create Lambda Execution Role
```bash
# Create Lambda execution role
aws iam create-role \
  --role-name LambdaExecutionRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'
```

### 4.2 Attach Policies to Lambda Role
```bash
# Attach basic execution policy
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Attach Textract policy
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonTextractFullAccess
```

## Step 5: GitHub Repository Configuration

### 5.1 No Secrets Required!
With OIDC, you don't need to store AWS credentials as GitHub secrets. The workflow uses the role directly.

### 5.2 Repository Settings
- Ensure the repository is public or you have GitHub Pro/Team for private repos
- The workflow will automatically use OIDC authentication

## Step 6: Workflow Configuration

### 6.1 Current Workflow Setup
The workflow is already configured to use OIDC:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::314146297130:role/OIDCRole_iamadmin_general
    aws-region: us-east-1
```

### 6.2 Environment Variables
The workflow uses these environment variables:
- `AWS_REGION`: us-east-1
- `LAMBDA_FUNCTION_NAME`: resume-analyzer
- `LAMBDA_RUNTIME`: python3.13
- `LAMBDA_HANDLER`: lambda_handler.lambda_handler

## Step 7: Testing the Setup

### 7.1 Test OIDC Authentication
```bash
# Test if the role can be assumed
aws sts get-caller-identity --role-arn arn:aws:iam::314146297130:role/OIDCRole_iamadmin_general --role-session-name test
```

### 7.2 Test Lambda Permissions
```bash
# Test Lambda permissions
aws lambda list-functions --region us-east-1
```

## Step 8: Security Best Practices

### 8.1 Principle of Least Privilege
- Only grant the minimum permissions needed
- Use resource-specific ARNs when possible
- Regularly audit permissions

### 8.2 Trust Policy Conditions
- Restrict to specific repositories
- Use branch-based conditions if needed
- Consider environment-based restrictions

### 8.3 Monitoring
- Enable CloudTrail for API calls
- Set up CloudWatch alarms
- Monitor IAM role usage

## Step 9: Troubleshooting

### Common Issues

#### 1. "Access Denied" Errors
- Check IAM role permissions
- Verify trust policy conditions
- Ensure OIDC provider is configured correctly

#### 2. "Role Not Found" Errors
- Verify role ARN is correct
- Check if role exists in the correct region
- Ensure role is not deleted

#### 3. "Invalid Token" Errors
- Check GitHub repository name in trust policy
- Verify OIDC provider configuration
- Ensure workflow is running from correct branch

### Debug Commands
```bash
# Check current identity
aws sts get-caller-identity

# List Lambda functions
aws lambda list-functions

# Check IAM role
aws iam get-role --role-name OIDCRole_iamadmin_general
```

## Step 10: Production Considerations

### 10.1 Multiple Environments
Consider creating separate roles for:
- Development
- Staging
- Production

### 10.2 Branch Protection
Use trust policy conditions to restrict deployments:
```json
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:ref": "refs/heads/main"
  }
}
```

### 10.3 Cost Optimization
- Monitor Lambda execution costs
- Set up billing alerts
- Use provisioned concurrency only when needed

## Benefits of OIDC

✅ **Security**: No long-term credentials stored
✅ **Rotation**: Automatic token rotation
✅ **Audit**: Better audit trail
✅ **Compliance**: Meets security best practices
✅ **Simplicity**: No secret management

## Next Steps

1. **Verify Setup**: Test the OIDC configuration
2. **Deploy**: Push code to trigger GitHub Actions
3. **Monitor**: Check CloudWatch logs and metrics
4. **Optimize**: Adjust permissions and resources as needed

Your GitHub Actions workflow is now configured for secure, keyless AWS deployment! 🚀
