# Render Deployment Guide - Employee Policy Q&A System

Quick guide to deploy your RAG app to Render's free tier.

---

## Prerequisites

- ✅ GitHub account with your code pushed
- ✅ OpenAI API key
- ✅ `render.yaml` file (already created in this project)

---

## Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create Render Account

1. Go to **[render.com](https://render.com)**
2. Click **"Get Started for Free"**
3. **Sign up with GitHub** (recommended for easy repo access)

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account if prompted
3. Select the **EmployeePolicy_Q&A_System** repository
4. Configure:

| Setting | Value |
|---------|-------|
| Name | `employee-policy-qa` |
| Region | Oregon (or closest to you) |
| Branch | `main` |
| Runtime | **Docker** |
| Instance Type | **Free** |

### Step 4: Add Environment Variables

Before clicking "Create", scroll to **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |

### Step 5: Deploy

Click **"Create Web Service"**

Render will:
1. Clone your repo
2. Build the Docker image
3. Deploy to a URL like: `https://employee-policy-qa.onrender.com`

**First deployment takes 5-10 minutes.**

---

## CI/CD (Automatic!)

Every time you push to `main`, Render automatically:
1. Detects the change
2. Rebuilds the Docker image
3. Deploys with zero downtime

No additional setup needed!

---

## Free Tier Notes

| Feature | Limit |
|---------|-------|
| RAM | 512 MB |
| Sleep | After 15 min inactivity |
| Wake time | ~30 seconds |
| Build minutes | 500/month |

---

## Test Your Deployment

1. Open your Render URL
2. Ask: "What is the probation period?"
3. Check health: `https://your-app.onrender.com/health`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Render logs for errors |
| App crashes | Verify OPENAI_API_KEY is set |
| Slow first load | Normal - free tier sleeping |
