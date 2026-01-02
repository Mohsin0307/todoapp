# 🚀 Deployment Guide - Hackathon Todo App

**Last Updated**: 2026-01-02
**Status**: ✅ Signup Fixed, Ready for Deployment

---

## ✅ SIGNUP FIX - What Was Done

### The Problem
- Frontend signup was showing "Failed to fetch" error
- Better Auth was trying to connect to port 8000 (not running)
- Demo backend on port 8002 didn't have auth endpoints

### The Solution
1. **Added Mock Auth Endpoints** to `backend/demo_chatbot.py`:
   - `/api/auth/sign-up/email` - Better Auth signup format
   - `/api/auth/sign-in/email` - Better Auth signin format
   - `/api/auth/session` - Session verification

2. **Updated Environment Variables** in `frontend/.env.local`:
   - Changed `NEXT_PUBLIC_API_URL` from port 8000 → 8002

3. **Restarted Both Servers**:
   - Backend demo server on port 8002
   - Frontend Next.js server on port 3000

### Result
✅ Signup now works!
✅ Login now works!
✅ Chat interface works!
✅ Full demo is functional!

---

## 📦 Deployment to GitHub

### Step 1: Prepare Repository

First, create a `.gitignore` file to exclude sensitive data:

```bash
# Create .gitignore if it doesn't exist
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
frontend/node_modules/
backend/.venv/
backend/__pycache__/
**/__pycache__/
*.pyc

# Environment variables
.env
.env.local
.env.*.local
backend/.env
frontend/.env.local

# Build outputs
frontend/.next/
frontend/out/
backend/dist/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
.temp/

# Database
*.db
*.sqlite
EOF
```

### Step 2: Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "feat: AI-powered todo chatbot with Better Auth and MCP tools

- Backend: FastAPI demo server with mock auth endpoints
- Frontend: Next.js 15 chat interface
- Features: Natural language task management, signup/login
- Status: Hackathon demo ready"
```

### Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named: `hackathon-todo-chatbot`
3. **DO NOT** initialize with README (we already have one)
4. Click "Create repository"

### Step 4: Push to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hackathon-todo-chatbot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌐 Deployment to Vercel

### Prerequisites

1. Vercel account (sign up at https://vercel.com)
2. GitHub repository created (see above)

### Step 1: Prepare for Vercel

Create `vercel.json` in the root directory:

```bash
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "backend/demo_chatbot.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/demo_chatbot.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
EOF
```

### Step 2: Create Production Environment File

Create `frontend/.env.production`:

```bash
cat > frontend/.env.production << 'EOF'
# Production Environment Variables
# These will be set in Vercel dashboard

NEXT_PUBLIC_API_URL=https://your-app-name.vercel.app
BETTER_AUTH_SECRET=
BETTER_AUTH_URL=https://your-app-name.vercel.app
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_APP_NAME=Hackathon Todo
EOF
```

### Step 3: Deploy to Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure Project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL = https://your-app-name.vercel.app
   BETTER_AUTH_SECRET = [generate with: openssl rand -base64 32]
   BETTER_AUTH_URL = https://your-app-name.vercel.app
   NEXT_PUBLIC_ENVIRONMENT = production
   ```

5. Click "Deploy"

#### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: hackathon-todo-chatbot
# - Directory: ./
# - Override settings? No

# Deploy to production
vercel --prod
```

### Step 4: Configure Backend on Vercel

**Important**: The demo backend (`demo_chatbot.py`) won't work on Vercel's free tier because it needs a persistent server.

**Two Options**:

#### Option 1: Use Vercel Serverless Functions (Recommended for Demo)

Convert endpoints to serverless functions in `frontend/api/`:

```bash
mkdir -p frontend/pages/api/auth

# Create signup endpoint
cat > frontend/pages/api/auth/sign-up/email.ts << 'EOF'
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { name, email, password } = req.body

  // Mock response for demo
  res.status(200).json({
    user: {
      id: 'demo-user-id',
      email,
      name,
      createdAt: new Date().toISOString()
    },
    session: {
      token: 'demo-token-123',
      expiresAt: new Date().toISOString()
    }
  })
}
EOF
```

#### Option 2: Deploy Backend Separately (Full Version)

Use Railway.app or Render.com for the Python backend:

1. **Railway.app** (Free tier available):
   - Connect GitHub repo
   - Select `backend` directory
   - Add `Procfile`: `web: uvicorn demo_chatbot:app --host 0.0.0.0 --port $PORT`
   - Deploy

2. **Render.com** (Free tier available):
   - Create new Web Service
   - Connect GitHub repo
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python demo_chatbot.py`

Then update `NEXT_PUBLIC_API_URL` in Vercel to point to your backend URL.

---

## 🔧 Environment Variables Summary

### Frontend (Vercel Dashboard)

```
NEXT_PUBLIC_API_URL = https://your-backend-url.com
BETTER_AUTH_SECRET = [32+ character random string]
BETTER_AUTH_URL = https://your-app-name.vercel.app
NEXT_PUBLIC_ENVIRONMENT = production
NEXT_PUBLIC_APP_NAME = Hackathon Todo
```

### Backend (Railway/Render)

```
PORT = 8000
CORS_ORIGINS = https://your-app-name.vercel.app
```

---

## ✅ Pre-Deployment Checklist

- [ ] `.gitignore` excludes `.env` files
- [ ] No API keys in code (check with: `git grep -E "sk-|api[-_]key"`)
- [ ] Frontend `.env.production` created
- [ ] vercel.json configured
- [ ] Git repository created and pushed
- [ ] Environment variables ready to paste

---

## 🧪 Testing After Deployment

1. **Test Signup**:
   ```
   Visit: https://your-app-name.vercel.app/signup
   Create account with test email
   ```

2. **Test Chat**:
   ```
   Visit: https://your-app-name.vercel.app/chat
   Try: "add a task to test deployment"
   Try: "show my tasks"
   ```

3. **Test API Health**:
   ```
   curl https://your-backend-url.com/api/health
   ```

---

## 📝 Deployment Notes

### Current Demo Mode

- Uses in-memory storage (resets on restart)
- Mock authentication (all logins succeed)
- No database persistence
- Perfect for hackathon demo!

### Production Version (Future)

To deploy the full version with real database:

1. Use Python 3.11 environment
2. Deploy PostgreSQL (Neon, Supabase, or AWS RDS)
3. Add Anthropic API key
4. Run migrations: `alembic upgrade head`
5. Use production backend endpoints

---

## 🆘 Troubleshooting

### "Failed to fetch" on Vercel

**Cause**: CORS or API URL mismatch

**Fix**:
1. Check `NEXT_PUBLIC_API_URL` points to correct backend
2. Ensure backend CORS allows your Vercel domain
3. Check browser console for exact error

### Environment Variables Not Working

**Cause**: Next.js requires rebuild after env var changes

**Fix**:
1. In Vercel dashboard: Settings → Environment Variables
2. Update variables
3. Trigger redeploy: Deployments → ... → Redeploy

### Backend Not Responding

**Cause**: Free tier sleep on Railway/Render

**Fix**:
1. First request may take 30-60 seconds (cold start)
2. Consider keeping backend awake with a ping service
3. Or use Vercel Serverless Functions instead

---

## 🎉 Success!

Once deployed, your app will be accessible at:

- **Frontend**: `https://your-app-name.vercel.app`
- **Chat Interface**: `https://your-app-name.vercel.app/chat`
- **API Docs**: `https://your-backend-url.com/docs` (if using separate backend)

**Demo URLs to Share**:
- GitHub Repo: `https://github.com/YOUR_USERNAME/hackathon-todo-chatbot`
- Live Demo: `https://your-app-name.vercel.app`

---

**Happy Deploying!** 🚀

For questions or issues, check the Vercel deployment logs in the dashboard.
