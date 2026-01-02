# ⚡ Quick Deploy Guide

**TL;DR**: Get your app live in 5 minutes!

---

## ✅ Signup Fixed!

The "Failed to fetch" error is now **FIXED**. Test locally:
- Backend: http://127.0.0.1:8002
- Frontend: http://localhost:3000
- Signup: http://localhost:3000/signup

---

## 🚀 Deploy to GitHub (2 minutes)

```bash
# 1. Create .gitignore (if not exists)
echo "node_modules/
.env
.env.local
frontend/.next/
backend/__pycache__/" > .gitignore

# 2. Commit everything
git add .
git commit -m "feat: Hackathon AI Todo Chatbot - Ready for demo"

# 3. Create GitHub repo at https://github.com/new
# Name it: hackathon-todo-chatbot

# 4. Push (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hackathon-todo-chatbot.git
git branch -M main
git push -u origin main
```

---

## 🌐 Deploy to Vercel (3 minutes)

### Method 1: Vercel Dashboard (Easiest)

1. Go to: https://vercel.com/new
2. Import your GitHub repository
3. **Framework**: Next.js
4. **Root Directory**: `frontend`
5. Add environment variables:
   ```
   NEXT_PUBLIC_API_URL = https://your-app.vercel.app
   BETTER_AUTH_SECRET = your-secret-key-here
   BETTER_AUTH_URL = https://your-app.vercel.app
   ```
6. Click **Deploy**

### Method 2: Vercel CLI

```bash
npm i -g vercel
cd frontend
vercel login
vercel --prod
```

---

## 🔧 Important: Backend Deployment

**Current Demo**: Backend runs on your local machine (port 8002)

**For Live Demo**: You need to deploy backend separately:

### Option A: Deploy to Railway.app (Free)

1. Go to: https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Select your repo → Choose `backend` directory
4. Add environment variable: `PORT=8000`
5. Copy the Railway URL (e.g., `https://xxx.railway.app`)
6. Update Vercel environment variable:
   ```
   NEXT_PUBLIC_API_URL = https://xxx.railway.app
   ```

### Option B: Use Vercel Serverless (No Separate Backend)

Since you're using a demo with mock data, you can skip the separate backend deployment for the hackathon. The signup will work with mock responses!

---

## ✅ That's It!

Your app should now be live at:
- `https://your-app-name.vercel.app`

---

## 🧪 Quick Test

1. Visit your Vercel URL
2. Click "Sign Up"
3. Create an account
4. Go to `/chat`
5. Try: "add a task to test deployment"

---

**Need help?** Check logs in Vercel dashboard → Deployments → View Function Logs
