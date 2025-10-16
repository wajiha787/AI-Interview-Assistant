# 🚀 Google Gemini API Setup Guide

The AI Hiring Evaluation System now uses **Google Gemini API** instead of OpenAI!

## ✅ Benefits of Google Gemini:
- **FREE** with generous limits (1500 requests/day for free tier)
- **Fast** - Similar or better performance than GPT-3.5
- **Reliable** - No quota issues
- **Cost-effective** - Much cheaper than OpenAI for paid tier

## 📝 How to Get Your Google Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://aistudio.google.com/app/apikey**

### Step 2: Sign in with Google Account
- Use any Google account (Gmail)
- No credit card required for free tier!

### Step 3: Create API Key
1. Click **"Get API Key"** or **"Create API Key"**
2. Select **"Create API key in new project"** (recommended)
3. Copy the generated API key

### Step 4: Add to Your .env File
1. Open your `.env` file in the project root
2. Replace the line with:
   ```
   GOOGLE_API_KEY=YOUR_API_KEY_HERE
   ```
3. Save the file

## 🎯 Complete .env File Example

```env
GOOGLE_API_KEY=AIzaSyABC123DEF456GHI789JKL012MNO345PQR678
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-hiring-evaluation
```

## 🚀 Start the Application

After setting up your API key:

```bash
python start.py
```

## 📊 Free Tier Limits

Google Gemini Free Tier:
- **1,500 requests per day**
- **gemini-1.5-flash model** (Fast and efficient)
- No credit card required
- Perfect for development and testing

## 🔧 Troubleshooting

### Error: "GOOGLE_API_KEY environment variable not set"
- Make sure your `.env` file is in the project root directory
- Verify the API key is on a line starting with `GOOGLE_API_KEY=`
- Restart the application after updating `.env`

### API Key Not Working
- Check that you copied the entire key (usually starts with `AIza`)
- Make sure there are no spaces before or after the key
- Verify the API key is enabled at https://aistudio.google.com/app/apikey

## 💡 Need Help?

Visit the official documentation:
- **API Keys**: https://aistudio.google.com/app/apikey
- **Documentation**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing

---

**Note**: The system is now configured to use `gemini-1.5-flash` model which is optimized for speed and efficiency!

