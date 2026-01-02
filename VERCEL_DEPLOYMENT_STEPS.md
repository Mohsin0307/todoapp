# 🚀 Vercel Deployment Guide - Todo AI Chatbot

## ✅ Prerequisites Complete

- ✅ Code pushed to GitHub: https://github.com/Mohsin0307/todoapp
- ✅ vercel.json configuration created
- ✅ .gitignore properly configured (no secrets exposed)

---

## 🌐 Deploy to Vercel (5 Minutes)

### Step 1: Import Your GitHub Repository

1. Go to: **https://vercel.com/new**
2. Click **"Import Git Repository"**
3. Select **"Import from GitHub"**
4. Find and select your repository: **Mohsin0307/todoapp**
5. Click **"Import"**

### Step 2: Configure Project Settings

Vercel will auto-detect Next.js. Configure as follows:

**Framework Preset:**
- ✅ Should auto-detect: **Next.js**

**Root Directory:**
- Set to: **`frontend`** (click "Edit" next to Root Directory)
- This tells Vercel to deploy only the frontend folder

**Build Command** (auto-filled):
- `npm run build`

**Output Directory** (auto-filled):
- `.next`

**Install Command** (auto-filled):
- `npm install`

### Step 3: Configure Environment Variables

Click **"Environment Variables"** and add the following:

#### Required Variables:

| Name | Value | Notes |
|------|-------|-------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8002` | Demo backend URL (update after backend deployment) |
| `BETTER_AUTH_SECRET` | `[generate random]` | Use: `openssl rand -base64 32` |
| `BETTER_AUTH_URL` | `https://your-app.vercel.app` | Update after deployment |
| `NEXT_PUBLIC_ENVIRONMENT` | `production` | Production environment flag |

#### How to Generate BETTER_AUTH_SECRET:

**Option A: Use OpenSSL (recommended)**
```bash
openssl rand -base64 32
```

**Option B: Use Node.js**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**Option C: Use a random generator**
- Any 32+ character random string
- Example: `xK3mP9vR2wQ7tL5nB8cD1fG4hJ6sA0uY`

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for the build to complete
3. You'll get a URL like: `https://todoapp-xxxx.vercel.app`

### Step 5: Update Environment Variables (Post-Deployment)

1. Go to your Vercel project dashboard
2. Click **Settings** → **Environment Variables**
3. Update `BETTER_AUTH_URL` to your actual Vercel URL
4. Click **"Save"**
5. Trigger a **"Redeploy"** from the Deployments tab

---

## 🔧 Backend Deployment Options

Your frontend is now live! But it needs a backend. Choose one option:

### Option A: Deploy Backend to Railway.app (Free Tier)

**Best for hackathon demos - Simple and free!**

1. Go to: **https://railway.app**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose: **Mohsin0307/todoapp**
5. Railway will detect the Python app

**Configure:**
- Root Directory: **`backend`**
- Start Command: **`python demo_chatbot.py`**
- Add Environment Variable:
  - `PORT`: `8000`

6. Click **"Deploy"**
7. Copy your Railway URL (e.g., `https://todoapp-production-xxxx.railway.app`)

**Update Vercel:**
8. Go back to Vercel → Settings → Environment Variables
9. Update `NEXT_PUBLIC_API_URL` to your Railway URL
10. Redeploy

### Option B: Deploy Backend to Render.com (Free Tier)

1. Go to: **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - Name: `todoapp-backend`
   - Root Directory: `backend`
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python demo_chatbot.py`
5. Add Environment Variable:
   - `PORT`: `8000`
6. Click **"Create Web Service"**
7. Copy your Render URL
8. Update Vercel's `NEXT_PUBLIC_API_URL` and redeploy

### Option C: Use Demo Mode (Local Backend Only)

- Frontend will be deployed on Vercel
- Backend runs locally on your machine (port 8002)
- Good for testing, not for production
- Users can see the UI but won't be able to interact unless your backend is publicly accessible

---

## 🧪 Testing Your Deployment

### 1. Test Frontend

Visit your Vercel URL: `https://todoapp-xxxx.vercel.app`

**Expected:**
- ✅ Landing page loads
- ✅ Signup page accessible: `/signup`
- ✅ Login page accessible: `/login`
- ✅ Chat page accessible: `/chat`

### 2. Test Signup

1. Go to: `https://todoapp-xxxx.vercel.app/signup`
2. Create a test account:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
3. Click **"Sign Up"**

**Expected (Demo Mode):**
- ✅ Successfully creates account (mock auth)
- ✅ Redirects to chat or tasks page

### 3. Test Chat Interface

1. Go to: `https://todoapp-xxxx.vercel.app/chat`
2. Try these commands:
   - "help"
   - "add a task to test deployment"
   - "show my tasks"
   - "how am I doing?"

**Expected (Demo Mode):**
- ✅ Chat interface loads
- ✅ Messages send successfully
- ✅ Bot responds with task confirmations

**If Backend is Deployed:**
- ✅ Real AI responses from Anthropic Claude
- ✅ Tasks persist in database
- ✅ Full conversation history

---

## 📊 Deployment Status Dashboard

### Frontend (Vercel)
- **Status**: ✅ Ready to deploy
- **Repository**: https://github.com/Mohsin0307/todoapp
- **Framework**: Next.js 15
- **Auto-deploy**: ✅ Enabled (pushes to main trigger redeployment)

### Backend (Choose One)
- **Option A - Railway**: Free tier, easy setup, good for demos
- **Option B - Render**: Free tier, similar to Railway
- **Option C - Local**: Not publicly accessible

### Environment Variables Summary
```
# Vercel Frontend
NEXT_PUBLIC_API_URL=https://your-backend-url.com
BETTER_AUTH_SECRET=[32-char random string]
BETTER_AUTH_URL=https://todoapp-xxxx.vercel.app
NEXT_PUBLIC_ENVIRONMENT=production

# Backend (Railway/Render)
PORT=8000
ANTHROPIC_API_KEY=[your-api-key] # Optional, for production mode
DATABASE_URL=[postgres-url] # Optional, for production mode
```

---

## 🎯 Quick Commands

### View Deployment Logs (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# View logs
vercel logs
```

### Trigger Redeployment
1. Go to Vercel Dashboard
2. Click your project
3. Go to **"Deployments"** tab
4. Click **"..."** on latest deployment
5. Click **"Redeploy"**

### Rollback Deployment
1. Go to Vercel Dashboard
2. Click **"Deployments"**
3. Find a previous successful deployment
4. Click **"..."** → **"Promote to Production"**

---

## ⚠️ Common Issues & Solutions

### Issue 1: "API Connection Failed"

**Cause**: Backend URL not configured or backend not deployed

**Fix:**
1. Check `NEXT_PUBLIC_API_URL` in Vercel environment variables
2. Ensure backend is deployed and accessible
3. Test backend health: `curl https://your-backend-url.com/api/health`
4. Redeploy frontend after updating env vars

### Issue 2: "Better Auth Session Error"

**Cause**: `BETTER_AUTH_URL` not updated after deployment

**Fix:**
1. Go to Vercel → Settings → Environment Variables
2. Update `BETTER_AUTH_URL` to actual Vercel URL
3. Redeploy

### Issue 3: "Build Failed"

**Cause**: Missing dependencies or environment variables

**Fix:**
1. Check Vercel build logs
2. Ensure all required env vars are set
3. Verify `frontend/package.json` has all dependencies
4. Try redeploying

### Issue 4: "404 Not Found" on Chat Page

**Cause**: Next.js routing issue

**Fix:**
1. Verify `frontend/app/chat/page.tsx` exists
2. Check Vercel build logs for any errors
3. Ensure framework preset is set to "Next.js"

---

## 🚀 You're Ready to Deploy!

### Deployment Checklist

- ✅ GitHub repository: https://github.com/Mohsin0307/todoapp
- ✅ vercel.json configuration created
- ✅ Environment variables prepared
- ✅ Backend deployment option chosen
- ⏳ Deploy frontend to Vercel
- ⏳ Deploy backend (Railway/Render)
- ⏳ Update environment variables
- ⏳ Test deployment

### Next Steps

1. **Deploy Frontend**: Follow Step 1-4 above
2. **Deploy Backend**: Choose Option A or B
3. **Test Everything**: Run through testing section
4. **Share Your Demo**: `https://todoapp-xxxx.vercel.app`

---

## 🎉 Congratulations!

Once deployed, share your hackathon demo:

**Demo URL**: `https://todoapp-xxxx.vercel.app`
**GitHub**: https://github.com/Mohsin0307/todoapp
**Documentation**: Available in repository

**Features to Demo:**
- ✅ Natural language task management
- ✅ AI-powered chatbot interface
- ✅ User authentication
- ✅ Real-time conversation
- ✅ Task statistics and analytics

---

**Need Help?** Check deployment logs or review the documentation in your repository.

**Good luck with your hackathon presentation!** 🎊
