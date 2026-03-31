# 🚀 QUICK REFERENCE - Deploy Image Enhancer

## 3-STEP DEPLOYMENT

### Step 1: Verify (30 seconds)
```powershell
.\check_deployment_ready.ps1
```

### Step 2: Push to GitHub (2 minutes)
```powershell
.\push_to_github.ps1
```
OR manually:
```powershell
git init
git add .
git commit -m "Initial Commit"
git remote add origin [YOUR_GITHUB_URL]
git push -u origin main
```

### Step 3: Deploy on Render (3-5 minutes)
1. https://render.com → Sign up
2. Create "New Web Service"
3. Select your GitHub repo: `image-enhancer`
4. Fill in:
   - Build: `pip install -r requirements.txt`
   - Start: `streamlit run src/interfaces/streamlit_app.py --server.port 10000 --server.address 0.0.0.0`
5. Environment Variables (add these):
   ```
   STREAMLIT_SERVER_PORT=10000
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   STREAMLIT_SERVER_HEADLESS=true
   FLASK_DEBUG=False
   ```
6. Click "Create Web Service"
7. Wait for build (2-3 minutes)
8. Get your public URL! 🎉

---

## WHAT WAS PREPARED

| Item | Status |
|------|--------|
| `.streamlit/config.toml` | ✅ Created |
| `runtime.txt` | ✅ Created |
| `requirements.txt` | ✅ Updated |
| `config.py` | ✅ Updated (env vars) |
| `.env.example` | ✅ Created |
| `DEPLOYMENT.md` | ✅ Created |
| `push_to_github.ps1` | ✅ Created |
| `check_deployment_ready.ps1` | ✅ Created |
| `README.md` | ✅ Updated |

---

## IMPORTANT FILES

📄 **DEPLOYMENT.md** - Read this! Full deployment guide
📄 **DEPLOYMENT_CHECKLIST.md** - Pre/post deployment checks
📄 **README.md** - Updated with deployment section
📄 **.env.example** - Environment variables reference

---

## LOCAL TESTING (Before Deploy)

```powershell
# Streamlit
streamlit run src/interfaces/streamlit_app.py

# Flask API
python deploy.py flask

# CLI
python main.py
```

---

## GITHUB COMMANDS

```powershell
# One-time setup
git init
git config user.email "you@example.com"
git config user.name "Your Name"

# Add & commit
git add .
git commit -m "Initial Commit"

# First push
git remote add origin https://github.com/YOUR_USERNAME/image-enhancer.git
git push -u origin main

# Future updates
git add .
git commit -m "Initial Commit"
git push
```

---

## RENDER SETTINGS SUMMARY

| Setting | Value |
|---------|-------|
| **Language** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run src/interfaces/streamlit_app.py --server.port 10000 --server.address 0.0.0.0` |
| **Python Version** | 3.11.8 (from runtime.txt) |
| **Port** | 10000 |
| **Plan** | Starter (Free) or Standard ($7/mo) |

---

## TROUBLESHOOTING

**App won't build:**
- Check `requirements.txt` for typos
- Verify internet connection
- Check Render logs

**App won't start:**
- Verify port is 10000
- Check `.streamlit/config.toml`
- Review stream logs for errors

**Slow performance:**
- Upgrade to Standard plan
- Check image sizes
- Optimize batch processing

---

## URLs AFTER DEPLOYMENT

- **Streamlit**: `https://image-enhancer-xxxxx.onrender.com`
- **Flask API** (if deployed separately): `https://image-enhancer-api-xxxxx.onrender.com`

---

## NEXT ACTIONS

1. ✅ Run: `.\check_deployment_ready.ps1`
2. ✅ Run: `.\push_to_github.ps1`
3. ✅ Go to: https://render.com
4. ✅ Follow 6 steps above
5. ✅ Share your deployed URL!

---

**Total Time to Live:** ~10 minutes ⏱️

Your project is ready! 🎉
