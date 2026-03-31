# 🚀 DEPLOYMENT GUIDE - Image Enhancement Project

## Quick Start for Render.com Deployment

### 1. **Push to GitHub**
```bash
cd c:\Image enhancer
git init
git add .
git commit -m "Initial Commit"
git remote add origin https://github.com/YOUR_USERNAME/image-enhancer.git
git push -u origin main
```

### 2. **Deploy to Render**

#### Option A: Streamlit Interface (Recommended)
1. Create account at https://render.com
2. Connect your GitHub repository
3. Create new "Web Service"
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run src/interfaces/streamlit_app.py --server.port 10000 --server.address 0.0.0.0`
   - **Environment:** Python 3

#### Option B: Flask API
1. Same setup as above, but use:
   - **Start Command:** `gunicorn --bind 0.0.0.0:10000 src.interfaces.flask_app:app`

### 3. **Environment Variables (in Render Dashboard)**
Add these in Service Settings → Environment:
```
STREAMLIT_SERVER_PORT=10000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
FLASK_DEBUG=False
DEPLOYMENT_MODE=production
```

### 4. **Files Prepared for Deployment**
✅ `.streamlit/config.toml` - Streamlit production config
✅ `runtime.txt` - Python version specification
✅ `requirements.txt` - All dependencies + gunicorn
✅ `config.py` - Environment variable support
✅ `.env.example` - Reference environment variables
✅ `.gitignore` - Ignore unnecessary files

### 5. **Expected Deploy Time**
- Initial build: 2-3 minutes
- Subsequent deploys: 1-2 minutes
- Auto-deploy on GitHub push: Enabled

### 6. **Access Your App**
Once deployed:
- Streamlit: `https://your-app.onrender.com`
- Flask API: `https://your-api.onrender.com`
- Direct link from Render Dashboard

### 7. **Troubleshooting**

**App won't start:**
- Check Render logs for errors
- Verify all packages in requirements.txt
- Ensure config.py doesn't have hardcoded paths

**Slow Performance:**
- Upgrade to Standard plan ($7/month)
- Add caching for images

**Out of Memory:**
- Reduce image processing batch size
- Upgrade to larger plan

---

## Files Modified/Created

| File | Purpose |
|------|---------|
| `.streamlit/config.toml` | ✨ NEW - Streamlit production settings |
| `runtime.txt` | ✨ NEW - Python version for Render |
| `.env.example` | ✨ NEW - Environment variables template |
| `requirements.txt` | 📝 UPDATED - Added gunicorn, python-dotenv |
| `config.py` | 📝 UPDATED - Environment variable support |
| `.gitignore` | ✓ Already configured |

---

## Next Steps

1. **Commit and push:**
   ```bash
   git add .
   git commit -m "Initial Commit"
   git push
   ```

2. **Create Render account:** https://render.com

3. **Connect GitHub and deploy** (Follow Step 2 above)

4. **Share your deployed URL!**

---

## Local Testing Before Deploy

Test everything locally first:

```bash
# Streamlit
streamlit run src/interfaces/streamlit_app.py

# Flask
python deploy.py flask

# CLI
python main.py
```

---

## Support

For issues:
- Check `.streamlit/config.toml` settings
- Review `requirements.txt` completeness
- See `config.py` for deployment mode
- Check Render logs for errors
