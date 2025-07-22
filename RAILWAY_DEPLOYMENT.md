# Railway Deployment Guide

## 🚀 **Quick Deploy to Railway**

### **Step 1: Prepare Your Repository**

Your repository is already prepared with:
- ✅ `api_prod.py` - Production-optimized FastAPI app
- ✅ `requirements-prod.txt` - Compatible dependencies
- ✅ `Dockerfile` - Docker configuration
- ✅ `railway.json` - Railway configuration

### **Step 2: Deploy to Railway**

1. **Go to Railway Dashboard**:
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `parkinsons-detection` repository

3. **Configure Deployment**:
   - Railway will automatically detect the Dockerfile
   - The `railway.json` file will configure the deployment
   - No additional configuration needed!

4. **Deploy**:
   - Click "Deploy Now"
   - Railway will build and deploy your API

### **Step 3: Access Your API**

Once deployed, Railway will provide:
- **Production URL**: `https://your-app-name.railway.app`
- **Health Check**: `https://your-app-name.railway.app/health`
- **API Docs**: `https://your-app-name.railway.app/docs`

## 📋 **API Endpoints**

Your deployed API will have these endpoints:

### **GET /** - API Information
```bash
curl https://your-app-name.railway.app/
```

### **GET /health** - Health Check
```bash
curl https://your-app-name.railway.app/health
```

### **GET /info** - Model Information
```bash
curl https://your-app-name.railway.app/info
```

### **POST /predict** - Make Predictions
```bash
curl -X POST -F "file=@your_data.csv" https://your-app-name.railway.app/predict
```

### **POST /analyze** - Data Analysis
```bash
curl -X POST -F "file=@your_data.csv" https://your-app-name.railway.app/analyze
```

### **POST /train** - Retrain Models
```bash
curl -X POST -F "file=@your_data.csv" https://your-app-name.railway.app/train
```

## 🔧 **Troubleshooting**

### **Common Issues**:

1. **Build Fails**:
   - Check Railway logs for specific errors
   - Ensure all files are committed to GitHub
   - Verify `requirements-prod.txt` is present

2. **API Not Responding**:
   - Check the health endpoint: `/health`
   - Review Railway logs for startup errors
   - Verify the deployment URL is correct

3. **Model Loading Issues**:
   - Ensure `data/parkinsons.data` is in the repository
   - Check file permissions
   - Review startup logs for data loading errors

### **Railway Logs**:
- Go to your project in Railway dashboard
- Click on the deployment
- View "Logs" tab for detailed information

## 📊 **Expected Performance**

- **Startup Time**: 30-60 seconds (model loading)
- **Memory Usage**: ~500MB
- **Response Time**: <1 second per prediction
- **Concurrent Requests**: 10-50 (depending on plan)

## 🎯 **Next Steps After Deployment**

1. **Test Your API**:
   ```bash
   curl https://your-app-name.railway.app/health
   ```

2. **Upload Sample Data**:
   - Use the `/predict` endpoint with your CSV data
   - Test with the provided dataset

3. **Monitor Performance**:
   - Check Railway dashboard for usage metrics
   - Monitor response times
   - Set up alerts if needed

4. **Scale if Needed**:
   - Railway auto-scales based on traffic
   - Upgrade plan for higher limits

## 🔒 **Security Considerations**

- Update CORS settings in `api_prod.py` for production
- Add authentication if needed
- Use HTTPS (Railway provides this automatically)
- Consider rate limiting for public APIs

Your API is now ready for production use! 🚀 