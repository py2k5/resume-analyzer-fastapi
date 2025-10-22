# Lambda + Namecheap Domain Deployment Guide

## Overview
This guide will help you deploy your Resume Analyzer as an AWS Lambda function and connect it to your Namecheap domain.

## Architecture
```
User Request → Namecheap Domain → AWS API Gateway → Lambda Function → AWS Textract
```

## Step 1: Prepare Lambda Package

### 1.1 Run Deployment Script
```bash
./deploy_lambda.sh
```
This creates `resume-analyzer-lambda.zip` ready for upload.

### 1.2 Manual Package Creation (Alternative)
```bash
# Create deployment directory
mkdir lambda_deployment
cd lambda_deployment

# Install dependencies
pip install -r ../requirements.txt -t .

# Copy application files
cp -r ../utils/ .
cp -r ../templates/ .
cp -r ../static/ .
cp ../main.py .
cp ../lambda_handler.py .

# Create zip
zip -r ../resume-analyzer-lambda.zip .
```

## Step 2: Create Lambda Function

### 2.1 Upload to AWS Lambda
1. Go to AWS Lambda Console
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `resume-analyzer`
5. Runtime: Python 3.9 or 3.10
6. Upload `resume-analyzer-lambda.zip`

### 2.2 Configure Lambda Settings
```yaml
Handler: lambda_handler.lambda_handler
Memory: 1024 MB (recommended for Textract)
Timeout: 30 seconds
Environment Variables:
  - AWS_DEFAULT_REGION: us-east-1
  - AWS_ACCESS_KEY_ID: (if not using IAM role)
  - AWS_SECRET_ACCESS_KEY: (if not using IAM role)
```

### 2.3 IAM Role Permissions
Attach these policies to your Lambda execution role:
- `AWSLambdaBasicExecutionRole`
- `AmazonTextractFullAccess`
- Custom policy for Textract (see AWS_SETUP_GUIDE.md)

## Step 3: Create API Gateway

### 3.1 Create REST API
1. Go to API Gateway Console
2. Click "Create API" → "REST API"
3. Choose "New API"
4. API name: `resume-analyzer-api`

### 3.2 Configure Resources and Methods
```yaml
Resources:
  /:
    GET: Lambda Function (resume-analyzer)
  /analyze:
    POST: Lambda Function (resume-analyzer)
  /static/{proxy+}:
    GET: Lambda Function (resume-analyzer)
```

### 3.3 Enable CORS
For each method, enable CORS:
```json
{
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
}
```

### 3.4 Deploy API
1. Click "Actions" → "Deploy API"
2. Deployment stage: `prod`
3. Note the API Gateway URL (e.g., `https://abc123.execute-api.us-east-1.amazonaws.com/prod`)

## Step 4: Configure Custom Domain

### 4.1 Create Custom Domain in API Gateway
1. Go to API Gateway → Custom Domain Names
2. Click "Create Custom Domain Name"
3. Domain name: `api.yourdomain.com` (or your preferred subdomain)
4. Certificate: Upload or select ACM certificate

### 4.2 Get ACM Certificate
1. Go to AWS Certificate Manager
2. Request a public certificate
3. Domain: `yourdomain.com` (or `*.yourdomain.com` for wildcard)
4. Validation: DNS validation (recommended)

### 4.3 Configure Domain Mapping
1. In Custom Domain Names, click your domain
2. Add base path mapping:
   - API: `resume-analyzer-api`
   - Stage: `prod`
   - Path: (leave empty for root)

## Step 5: Configure Namecheap DNS

### 5.1 Add DNS Records
In your Namecheap DNS management:

#### Option A: Subdomain (Recommended)
```
Type: CNAME
Host: api
Value: d-abc123.execute-api.us-east-1.amazonaws.com
TTL: 300
```

#### Option B: Root Domain
```
Type: A
Host: @
Value: [API Gateway IP] (use ALIAS if available)
TTL: 300
```

### 5.2 Verify DNS Propagation
```bash
# Check DNS resolution
nslookup api.yourdomain.com
dig api.yourdomain.com
```

## Step 6: Test Deployment

### 6.1 Test Lambda Function
```bash
# Test via API Gateway URL
curl https://abc123.execute-api.us-east-1.amazonaws.com/prod/

# Test via custom domain
curl https://api.yourdomain.com/
```

### 6.2 Test File Upload
```bash
curl -X POST \
  -F "file=@resume.pdf" \
  https://api.yourdomain.com/analyze
```

## Step 7: Production Optimizations

### 7.1 Lambda Configuration
```yaml
Memory: 1024 MB
Timeout: 30 seconds
Reserved Concurrency: 10 (adjust based on usage)
Environment Variables:
  - LOG_LEVEL: INFO
  - AWS_DEFAULT_REGION: us-east-1
```

### 7.2 API Gateway Optimizations
- Enable API caching (if appropriate)
- Set up CloudWatch monitoring
- Configure throttling limits

### 7.3 Cost Optimization
- Use Provisioned Concurrency only if needed
- Monitor Lambda execution time
- Set up billing alerts

## Step 8: Monitoring and Logging

### 8.1 CloudWatch Logs
- Lambda logs automatically go to CloudWatch
- Set up log retention policy
- Create log-based metrics

### 8.2 API Gateway Logs
- Enable execution logging
- Monitor API usage and errors
- Set up CloudWatch alarms

## Step 9: Security Considerations

### 9.1 API Security
- Use API keys for production
- Implement rate limiting
- Enable AWS WAF if needed

### 9.2 Lambda Security
- Use IAM roles instead of access keys
- Enable VPC if needed
- Regular security updates

## Troubleshooting

### Common Issues

#### 1. CORS Errors
```python
# Ensure CORS headers in Lambda response
{
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
}
```

#### 2. Lambda Timeout
- Increase timeout in Lambda configuration
- Optimize code for faster execution
- Use async processing for large files

#### 3. DNS Issues
- Check DNS propagation: `dig yourdomain.com`
- Verify CNAME/A record configuration
- Wait for DNS cache to clear

#### 4. SSL Certificate Issues
- Ensure certificate covers your domain
- Check certificate validation status
- Verify DNS validation records

## Cost Estimation

### Monthly Costs (Approximate)
- Lambda: $0.20 per 1M requests + $0.0000166667 per GB-second
- API Gateway: $3.50 per 1M requests
- Textract: $1.50 per 1,000 pages
- CloudWatch: $0.50 per GB of logs

### Example (1,000 resumes/month)
- Lambda: ~$0.50
- API Gateway: ~$3.50
- Textract: ~$1.50
- **Total: ~$5.50/month**

## Next Steps

1. **Deploy**: Run `./deploy_lambda.sh` and upload to Lambda
2. **Configure**: Set up API Gateway and custom domain
3. **DNS**: Update Namecheap DNS records
4. **Test**: Verify everything works
5. **Monitor**: Set up CloudWatch alarms
6. **Scale**: Adjust concurrency based on usage

## Support Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [Namecheap DNS Guide](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain)
- [Mangum Documentation](https://mangum.io/)

Your Resume Analyzer will be live at `https://api.yourdomain.com` once deployed! 🚀
