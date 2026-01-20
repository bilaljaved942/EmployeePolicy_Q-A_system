#!/bin/bash

# AWS Setup Script for Employee Policy Q&A System
# Run this script to set up all AWS resources

set -e

REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Setting up AWS resources for Employee Policy Q&A System..."
echo "Region: $REGION"
echo "Account ID: $ACCOUNT_ID"

# 1. Create ECR Repository
echo "Creating ECR repository..."
aws ecr create-repository \
    --repository-name employee-policy-qa \
    --region $REGION \
    --image-scanning-configuration scanOnPush=true \
    || echo "Repository already exists"

# 2. Create EFS File System
echo "Creating EFS file system..."
EFS_ID=$(aws efs create-file-system \
    --creation-token employee-policy-efs \
    --region $REGION \
    --query 'FileSystemId' --output text 2>/dev/null || \
    aws efs describe-file-systems \
    --creation-token employee-policy-efs \
    --region $REGION \
    --query 'FileSystems[0].FileSystemId' --output text)

echo "EFS File System ID: $EFS_ID"

# 3. Create CloudWatch Log Group
echo "Creating CloudWatch log group..."
aws logs create-log-group \
    --log-group-name /ecs/employee-policy-qa \
    --region $REGION \
    || echo "Log group already exists"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create ECS cluster: aws ecs create-cluster --cluster-name employee-policy-cluster --region $REGION"
echo "2. Create task definition using task-definition.json"
echo "3. Create ALB and target group"
echo "4. Create ECS service"
echo "5. Add GitHub secrets for CI/CD"
