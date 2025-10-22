#!/bin/bash

# Comprehensive Lambda Execution Role Setup Script
# This script creates the required IAM role for Lambda with proper permissions

set -e

echo "🔧 Setting up Lambda execution role for Resume Analyzer..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo "❌ AWS CLI not configured or credentials expired"
    echo "Please run: aws sso login"
    echo "Or configure AWS credentials: aws configure"
    exit 1
fi

echo "✅ AWS CLI is configured"

# Get current account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "📋 AWS Account ID: $ACCOUNT_ID"

# Create Lambda execution role
echo "Creating Lambda execution role..."
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
  }' \
  2>/dev/null && echo "✅ Role created" || echo "ℹ️  Role already exists"

# Attach basic execution policy
echo "Attaching basic execution policy..."
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

echo "✅ Basic execution policy attached"

# Attach Textract policy
echo "Attaching Textract policy..."
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonTextractFullAccess

echo "✅ Textract policy attached"

# Create custom policy for additional permissions
echo "Creating custom policy for additional permissions..."
aws iam create-policy \
  --policy-name ResumeAnalyzerLambdaPolicy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      },
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
  }' \
  2>/dev/null && echo "✅ Custom policy created" || echo "ℹ️  Custom policy already exists"

# Attach custom policy
echo "Attaching custom policy..."
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/ResumeAnalyzerLambdaPolicy

echo "✅ Custom policy attached"

# Get role ARN
ROLE_ARN=$(aws iam get-role --role-name LambdaExecutionRole --query 'Role.Arn' --output text)
echo "🎯 Lambda execution role ARN: $ROLE_ARN"

# Verify role can be assumed by Lambda
echo "Verifying role trust policy..."
aws iam get-role --role-name LambdaExecutionRole --query 'Role.AssumeRolePolicyDocument'

echo ""
echo "✅ Lambda execution role setup complete!"
echo "The role ARN is: $ROLE_ARN"
echo ""
echo "Next steps:"
echo "1. Update your GitHub Actions workflow to use this role ARN"
echo "2. Push your changes to trigger deployment"
echo "3. Monitor the GitHub Actions logs for successful deployment"
