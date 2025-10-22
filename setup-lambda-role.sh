#!/bin/bash

# Script to create Lambda execution role for Resume Analyzer
# Run this script to set up the required IAM role for Lambda

set -e

echo "🔧 Setting up Lambda execution role..."

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
  2>/dev/null || echo "Role already exists"

echo "✅ Lambda execution role created/verified"

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

# Get role ARN
ROLE_ARN=$(aws iam get-role --role-name LambdaExecutionRole --query 'Role.Arn' --output text)
echo "🎯 Lambda execution role ARN: $ROLE_ARN"

echo ""
echo "✅ Lambda execution role setup complete!"
echo "The role ARN is: $ROLE_ARN"
echo "You can now deploy your Lambda function using GitHub Actions."
