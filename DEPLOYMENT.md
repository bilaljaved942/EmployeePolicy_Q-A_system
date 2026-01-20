# Deployment Guide - Employee Policy Q&A System

This guide will walk you through deploying your RAG-based Q&A system to AWS with CI/CD pipeline.

## Architecture Overview

```
GitHub Repository
    ↓ (Push/PR)
GitHub Actions (CI/CD)
    ↓ (Build & Deploy)
AWS ECS/Fargate (Container)
    ↓
Application (FastAPI)
    ↓
ChromaDB (Vector DB) → EFS (Persistent Storage)
```

## Prerequisites

- AWS Account
- GitHub Account
- Docker installed locally
- AWS CLI installed and configured
- Basic knowledge of AWS services

---

## Step 1: Prepare Your Application for Deployment

### 1.1 Create Dockerfile

Create a `Dockerfile` in the root directory:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data
RUN mkdir -p vector_db documents

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.2 Create .dockerignore

Create `.dockerignore`:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.git
.gitignore
.env
*.md
.DS_Store
vector_db/*
!vector_db/.gitkeep
```

### 1.3 Update app.py for Production

Update `app.py` to handle production settings:

```python
# Add at the top of app.py
import os

# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update uvicorn run command
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 1.4 Create docker-compose.yml (for local testing)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PORT=8000
    volumes:
      - ./vector_db:/app/vector_db
      - ./documents:/app/documents
    restart: unless-stopped
```

---

## Step 2: AWS Setup

### 2.1 Create AWS Resources

#### Option A: AWS ECS with Fargate (Recommended - Serverless)

**Services Needed:**
- **ECS (Elastic Container Service)** - Container orchestration
- **ECR (Elastic Container Registry)** - Docker image storage
- **EFS (Elastic File System)** - Persistent storage for vector DB
- **Application Load Balancer** - Load balancing
- **Route 53** (Optional) - Domain management
- **ACM (AWS Certificate Manager)** - SSL certificates
- **IAM Roles** - Permissions

#### Option B: AWS EC2 (Simpler but requires management)

**Services Needed:**
- **EC2 Instance** - Virtual server
- **Security Groups** - Firewall rules
- **Elastic IP** - Static IP address
- **Route 53** (Optional) - Domain

---

## Step 3: Detailed Deployment Steps

### Step 3.1: Create ECR Repository

```bash
# Login to AWS
aws configure

# Create ECR repository
aws ecr create-repository --repository-name employee-policy-qa --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

### Step 3.2: Create EFS for Vector DB Storage

```bash
# Create EFS file system
aws efs create-file-system --creation-token employee-policy-efs --region us-east-1

# Note the FileSystemId from output
# Create mount targets in your VPC subnets
aws efs create-mount-target \
    --file-system-id <FILE_SYSTEM_ID> \
    --subnet-id <SUBNET_ID> \
    --security-groups <SECURITY_GROUP_ID> \
    --region us-east-1
```

### Step 3.3: Create ECS Cluster

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name employee-policy-cluster --region us-east-1
```

### Step 3.4: Create Task Definition

Create `task-definition.json`:

```json
{
  "family": "employee-policy-qa",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "employee-policy-qa",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/employee-policy-qa:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "YOUR_OPENAI_API_KEY"
        },
        {
          "name": "PORT",
          "value": "8000"
        }
      ],
      "mountPoints": [
        {
          "sourceVolume": "vector-db",
          "containerPath": "/app/vector_db"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/employee-policy-qa",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "volumes": [
    {
      "name": "vector-db",
      "efsVolumeConfiguration": {
        "fileSystemId": "<EFS_FILE_SYSTEM_ID>",
        "rootDirectory": "/"
      }
    }
  ]
}
```

### Step 3.5: Create Application Load Balancer

```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name employee-policy-alb \
    --subnets <SUBNET_ID_1> <SUBNET_ID_2> \
    --security-groups <SECURITY_GROUP_ID> \
    --region us-east-1
```

---

## Step 4: CI/CD Pipeline Setup

### Step 4.1: GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS ECS

on:
  push:
    branches:
      - main

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: employee-policy-qa
  ECS_SERVICE: employee-policy-qa-service
  ECS_CLUSTER: employee-policy-cluster
  ECS_TASK_DEFINITION: employee-policy-qa

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build, tag, and push image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

    - name: Download task definition
      run: |
        aws ecs describe-task-definition \
          --task-definition ${{ env.ECS_TASK_DEFINITION }} \
          --query taskDefinition > task-definition.json

    - name: Fill in the new image ID in the Amazon ECS task definition
      id: task-def
      uses: aws-actions/amazon-ecs-render-task-definition@v1
      with:
        task-definition: task-definition.json
        container-name: employee-policy-qa
        image: ${{ steps.build-image.outputs.image }}

    - name: Deploy Amazon ECS task definition
      uses: aws-actions/amazon-ecs-deploy-task-definition@v1
      with:
        task-definition: ${{ steps.task-def.outputs.task-definition }}
        service: ${{ env.ECS_SERVICE }}
        cluster: ${{ env.ECS_CLUSTER }}
        wait-for-service-stability: true
```

### Step 4.2: Add GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions:

Add these secrets:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `OPENAI_API_KEY` - Your OpenAI API key (or use AWS Secrets Manager)

---

## Step 5: AWS Secrets Manager (Recommended)

Instead of hardcoding API keys, use AWS Secrets Manager:

```bash
# Create secret for OpenAI API key
aws secretsmanager create-secret \
    --name employee-policy/openai-api-key \
    --secret-string "YOUR_OPENAI_API_KEY" \
    --region us-east-1
```

Update your task definition to use secrets:

```json
"secrets": [
  {
    "name": "OPENAI_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-1:<ACCOUNT_ID>:secret:employee-policy/openai-api-key"
  }
]
```

---

## Step 6: Create ECS Service

```bash
aws ecs create-service \
    --cluster employee-policy-cluster \
    --service-name employee-policy-qa-service \
    --task-definition employee-policy-qa \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SECURITY_GROUP_ID>],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=<TARGET_GROUP_ARN>,containerName=employee-policy-qa,containerPort=8000" \
    --region us-east-1
```

---

## Step 7: Domain and SSL Setup (Optional)

### 7.1 Route 53 Domain

1. Register domain in Route 53 or transfer existing domain
2. Create hosted zone
3. Create A record pointing to ALB

### 7.2 SSL Certificate

```bash
# Request certificate
aws acm request-certificate \
    --domain-name yourdomain.com \
    --validation-method DNS \
    --region us-east-1

# Add certificate to ALB listener
aws elbv2 create-listener \
    --load-balancer-arn <ALB_ARN> \
    --protocol HTTPS \
    --port 443 \
    --certificates CertificateArn=<CERTIFICATE_ARN> \
    --default-actions Type=forward,TargetGroupArn=<TARGET_GROUP_ARN>
```

---

## Step 8: Environment Variables Setup

Create `.env.production` template:

```env
OPENAI_API_KEY=your_key_here
ALLOWED_ORIGINS=https://yourdomain.com
PORT=8000
ENVIRONMENT=production
```

---

## Step 9: Monitoring and Logging

### 9.1 CloudWatch Logs

Logs are automatically sent to CloudWatch via the task definition.

### 9.2 CloudWatch Alarms

Create alarms for:
- CPU utilization
- Memory utilization
- Request count
- Error rate

---

## Step 10: Cost Optimization

### Estimated Monthly Costs (US East):

- **ECS Fargate**: ~$15-30/month (1 task, 1GB RAM)
- **ECR**: ~$0.10/month (storage)
- **EFS**: ~$3/month (1GB storage)
- **ALB**: ~$16/month (always running)
- **Data Transfer**: ~$0.09/GB

**Total: ~$35-50/month** (without domain)

---

## Quick Deployment Checklist

- [ ] Dockerfile created and tested locally
- [ ] ECR repository created
- [ ] EFS file system created
- [ ] ECS cluster created
- [ ] Task definition created
- [ ] IAM roles configured
- [ ] Security groups configured
- [ ] ALB created and configured
- [ ] GitHub Actions workflow created
- [ ] GitHub secrets added
- [ ] ECS service created
- [ ] Domain configured (optional)
- [ ] SSL certificate added (optional)
- [ ] Monitoring set up

---

## Alternative: Simpler EC2 Deployment

If ECS seems complex, you can deploy to EC2:

1. Launch EC2 instance (Ubuntu)
2. Install Docker
3. Clone repository
4. Run docker-compose
5. Configure security groups
6. Set up nginx reverse proxy
7. Use GitHub Actions to SSH and deploy

---

## Troubleshooting

### Common Issues:

1. **Container won't start**: Check CloudWatch logs
2. **EFS mount fails**: Verify security groups allow NFS
3. **Image pull fails**: Check ECR permissions
4. **ALB health checks failing**: Verify port 8000 is open

---

## Next Steps

1. Start with local Docker testing
2. Set up ECR and push image
3. Create ECS resources
4. Set up GitHub Actions
5. Deploy and test
6. Add monitoring

Need help with any specific step? Let me know!
