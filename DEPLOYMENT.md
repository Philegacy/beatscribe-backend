
## Files for Deployment

✅ **requirements.txt** - Contains all Python dependencies
✅ **render.yaml** - Render service configuration  
✅ **main.py** - FastAPI app with proper structure

## Deployment Steps

1. **Push to GitHub**: Make sure all files are committed to your repository

2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**:
   - In Render dashboard, go to your service settings
   - Add environment variable: `OPENROUTER_API_KEY` = your API key

4. **Deploy**: Render will automatically build and deploy using the configuration in `render.yaml`

## Configuration Details

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
- **Plan**: Free tier
- **Environment**: Python

## Health Check

Once deployed, your API will be available at:
- Main endpoint: `https://your-app-name.onrender.com/ai-lyric`
- Health check: `https://your-app-name.onrender.com/health`
- API docs: `https://your-app-name.onrender.com/docs`

## Environment Variables Needed

- `OPENROUTER_API_KEY`: Your OpenRouter API key for AI functionality
