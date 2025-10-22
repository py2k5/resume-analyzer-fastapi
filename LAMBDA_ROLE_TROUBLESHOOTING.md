# Lambda Role Setup Troubleshooting Guide

## Problem: "The role defined for the function cannot be assumed by Lambda"

This error occurs when the Lambda execution role doesn't exist or has incorrect permissions.

## Quick Fix Steps:

### 1. Refresh AWS Credentials
```bash
# If using AWS SSO
aws sso login

# If using AWS CLI
aws configure
```

### 2. Create Lambda Execution Role
```bash
# Run the setup script
./setup-lambda-role-complete.sh
```

### 3. Verify Role Creation
```bash
# Check if role exists
aws iam get-role --role-name LambdaExecutionRole

# Check role permissions
aws iam list-attached-role-policies --role-name LambdaExecutionRole
```

## Manual Role Creation (if script fails):

### 1. Create Role
```bash
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

### 2. Attach Policies
```bash
# Basic execution policy
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Textract policy
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonTextractFullAccess
```

### 3. Verify Role
```bash
# Get role ARN
aws iam get-role --role-name LambdaExecutionRole --query 'Role.Arn' --output text
```

## Common Issues:

### Issue 1: AWS Credentials Expired
**Solution:** Run `aws sso login` or `aws configure`

### Issue 2: Role Already Exists
**Solution:** The script handles this automatically

### Issue 3: Insufficient Permissions
**Solution:** Ensure your OIDC role has IAM permissions

### Issue 4: Wrong Account ID
**Solution:** Verify you're in the correct AWS account (314146297130)

## Verification Commands:

```bash
# Check current identity
aws sts get-caller-identity

# Check role exists
aws iam get-role --role-name LambdaExecutionRole

# Check role permissions
aws iam list-attached-role-policies --role-name LambdaExecutionRole

# Test role assumption (from Lambda service perspective)
aws lambda list-functions --max-items 1
```

## Next Steps After Fix:

1. **Push Changes**: Commit and push your code
2. **Monitor Deployment**: Watch GitHub Actions logs
3. **Test Function**: Verify Lambda function works
4. **Check Logs**: Monitor CloudWatch logs

## Role ARN Format:
```
arn:aws:iam::314146297130:role/LambdaExecutionRole
```

The GitHub Actions workflow will automatically detect your account ID and use the correct ARN.
