# Deployment Guide - Parkinson's Disease Detection API

This guide covers deploying the Parkinson's Disease Detection API to production environments.

## 🚀 **Quick Deploy Options**

### **Option 1: Railway (Recommended - Easiest)**

1. **Install Railway CLI** (optional):
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will automatically detect the Python app and deploy
   - Your API will be available at `https://your-app-name.railway.app`

3. **Environment Variables** (if needed):
   - Add any environment variables in Railway dashboard
   - The app will use the `$PORT` environment variable automatically

### **Option 2: Render**

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Deploy**:
   - Click "New Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Deploy!

### **Option 3: Heroku**

1. **Install Heroku CLI**:
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

### **Option 4: Docker Deployment**

1. **Build Docker Image**:
   ```bash
   docker build -t parkinsons-api .
   ```

2. **Run Locally**:
   ```bash
   docker run -p 8000:8000 parkinsons-api
   ```

3. **Deploy to Cloud**:
   - **Google Cloud Run**:
     ```bash
     gcloud run deploy parkinsons-api --image gcr.io/PROJECT_ID/parkinsons-api
     ```
   - **AWS ECS**: Use AWS CLI or console
   - **Azure Container Instances**: Use Azure CLI

## 📋 **API Endpoints**

Once deployed, your API will have these endpoints:

### **GET /** - API Information
```bash
curl https://your-app.railway.app/
```

### **GET /health** - Health Check
```bash
curl https://your-app.railway.app/health
```

### **GET /info** - Model Information
```bash
curl https://your-app.railway.app/info
```

### **POST /predict** - Make Predictions
```bash
curl -X POST -F "file=@your_data.csv" https://your-app.railway.app/predict
```

### **POST /analyze** - Data Analysis
```bash
curl -X POST -F "file=@your_data.csv" https://your-app.railway.app/analyze
```

### **POST /train** - Retrain Models
```bash
curl -X POST -F "file=@your_data.csv" https://your-app.railway.app/train
```

## 🔧 **Local Development**

### **Run Locally**:
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
python api.py

# Or with uvicorn
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### **Test API**:
```bash
python test_api.py
```

### **Access API Documentation**:
- Open your browser to `http://localhost:8000/docs`
- Interactive Swagger UI documentation

## 📊 **Expected Data Format**

The API expects CSV files with these columns:
- `name` - Patient identifier
- `MDVP:Fo(Hz)` - Average vocal fundamental frequency
- `MDVP:Fhi(Hz)` - Maximum vocal fundamental frequency
- `MDVP:Flo(Hz)` - Minimum vocal fundamental frequency
- `MDVP:Jitter(%)` - Jitter percentage
- `MDVP:Jitter(Abs)` - Absolute jitter
- `MDVP:RAP` - Relative average perturbation
- `MDVP:PPQ` - Five-point period perturbation quotient
- `Jitter:DDP` - Average absolute difference of differences
- `MDVP:Shimmer` - Shimmer
- `MDVP:Shimmer(dB)` - Shimmer in dB
- `Shimmer:APQ3` - Three-point amplitude perturbation quotient
- `Shimmer:APQ5` - Five-point amplitude perturbation quotient
- `MDVP:APQ` - Amplitude perturbation quotient
- `Shimmer:DDA` - Average absolute difference between consecutive differences
- `NHR` - Noise-to-harmonics ratio
- `HNR` - Harmonics-to-noise ratio
- `status` - Target variable (0 = healthy, 1 = Parkinson's)
- `RPDE` - Recurrence period density entropy
- `DFA` - Detrended fluctuation analysis
- `spread1` - Nonlinear measure of fundamental frequency variation
- `spread2` - Nonlinear measure of fundamental frequency variation
- `D2` - Correlation dimension
- `PPE` - Pitch period entropy

## 🔒 **Production Considerations**

### **Security**:
- Update CORS settings in `api.py` for production
- Add authentication if needed
- Use HTTPS in production

### **Performance**:
- The API loads models on startup (takes ~30 seconds)
- Consider model caching for faster startup
- Monitor memory usage

### **Monitoring**:
- Use the `/health` endpoint for health checks
- Monitor API response times
- Set up logging for production

### **Scaling**:
- Railway/Render auto-scale based on traffic
- For high traffic, consider container orchestration
- Use load balancers for multiple instances

## 🐛 **Troubleshooting**

### **Common Issues**:

1. **Port Issues**:
   - Ensure `$PORT` environment variable is set
   - Check if port 8000 is available locally

2. **Dependencies**:
   - Verify all packages in `requirements.txt`
   - Check Python version compatibility

3. **Model Loading**:
   - Ensure `data/parkinsons.data` is present
   - Check file permissions

4. **Memory Issues**:
   - Models require ~500MB RAM
   - Consider using lighter models for production

### **Logs**:
- Railway: View logs in dashboard
- Render: Check deployment logs
- Heroku: `heroku logs --tail`

## 📈 **Performance Metrics**

Typical performance:
- **Startup Time**: 30-60 seconds (model loading)
- **Prediction Time**: <1 second per sample
- **Memory Usage**: ~500MB
- **Concurrent Requests**: 10-50 (depending on platform)

## 🎯 **Next Steps**

1. **Deploy to Railway** (easiest)
2. **Test all endpoints**
3. **Set up monitoring**
4. **Add authentication if needed**
5. **Scale as needed**

Your API is now ready for production! 🚀 