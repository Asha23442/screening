# API Keys Setup Guide

This guide explains all the API keys needed for the Resume Screening Agent and how to get them.

## 🔴 Required Keys (Minimum to Run)

### 1. OpenAI API Key (REQUIRED)
**Purpose**: Primary AI model for resume screening

**How to get it:**
1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to **API Keys**: https://platform.openai.com/api-keys
4. Click **"Create new secret key"**
5. Copy the key immediately (you won't see it again!)
6. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Cost**: Pay-as-you-go (check pricing at https://openai.com/pricing)
- GPT-4 Turbo: ~$0.01 per 1K input tokens, $0.03 per 1K output tokens
- For resume screening: ~$0.10-0.50 per resume depending on length

**Note**: You can start with $5-10 credit to test the app

---

## 🟡 Alternative AI Models (Optional - Choose One)

You only need ONE of these if you don't want to use OpenAI:

### 2. Anthropic (Claude) API Key (OPTIONAL)
**Purpose**: Alternative AI model (Claude) for resume screening

**How to get it:**
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Go to **API Keys**: https://console.anthropic.com/settings/keys
4. Click **"Create Key"**
5. Copy the key
6. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Cost**: Pay-as-you-go
- Claude Opus: ~$0.015 per 1K input tokens, $0.075 per 1K output tokens

### 3. Google Gemini API Key (OPTIONAL)
**Purpose**: Alternative AI model (Gemini) for resume screening

**How to get it:**
1. Go to https://aistudio.google.com
2. Sign in with Google account
3. Click **"Get API Key"** in the left menu
4. Create a new API key or use existing
5. Copy the key
6. Add to `.env`: `GOOGLE_API_KEY=AIza...`

**Cost**: Free tier available, then pay-as-you-go
- Gemini Pro: Free tier includes generous limits

**Recommendation**: Start with Gemini if you want to test for free!

---

## 🟢 Database (Already Configured ✅)

### 4. Supabase URL & Key (ALREADY SET UP)
**Status**: ✅ Already configured in your `.env` file
- `SUPABASE_URL=https://kaodsueafxcnareczgni.supabase.co`
- `SUPABASE_KEY=eyJhbGci...` (your anon key)

**No action needed** - this is already working!

---

## 🔵 Optional Integrations (Not Required)

These are nice-to-have features but not needed to run the app:

### 5. Notion API Key (OPTIONAL)
**Purpose**: Export candidate data to Notion workspace

**How to get it:**
1. Go to https://www.notion.so/my-integrations
2. Click **"New integration"**
3. Name it (e.g., "Resume Screening")
4. Select your workspace
5. Copy the **Internal Integration Token**
6. Add to `.env`: `NOTION_API_KEY=secret_...`

**Cost**: Free

**When to use**: If you manage candidates in Notion

---

### 6. Google Calendar Credentials (OPTIONAL)
**Purpose**: Automatically schedule interviews

**How to get it:**
1. Go to https://console.cloud.google.com
2. Create a new project or select existing
3. Enable **Google Calendar API**
4. Go to **Credentials** → **Create Credentials** → **Service Account**
5. Download the JSON key file
6. Save it in your project folder
7. Add to `.env`: `GOOGLE_CALENDAR_CREDENTIALS=./path/to/credentials.json`

**Cost**: Free (with Google account)

**When to use**: If you want to auto-schedule interviews

---

### 7. Google Sheets Credentials (OPTIONAL)
**Purpose**: Export results to Google Sheets

**How to get it:**
1. Similar to Google Calendar setup
2. Enable **Google Sheets API** in Google Cloud Console
3. Create Service Account and download JSON
4. Add to `.env`: `GOOGLE_SHEETS_CREDENTIALS=./path/to/credentials.json`

**Cost**: Free (with Google account)

**When to use**: If you want to export results to spreadsheets

---

## 📋 Quick Setup Checklist

### Minimum Setup (To Run the App):
- [x] ✅ Supabase URL & Key (Already done!)
- [ ] ⬜ OpenAI API Key (Required)
- [ ] ⬜ OR Anthropic API Key (Alternative)
- [ ] ⬜ OR Google Gemini API Key (Alternative - Free tier available!)

### Recommended Setup:
- [x] ✅ Supabase (Done!)
- [ ] ⬜ OpenAI API Key (Best quality)
- [ ] ⬜ Google Gemini API Key (Free alternative for testing)

### Full Setup (All Features):
- [x] ✅ Supabase
- [ ] ⬜ OpenAI/Claude/Gemini (at least one)
- [ ] ⬜ Notion API Key
- [ ] ⬜ Google Calendar Credentials
- [ ] ⬜ Google Sheets Credentials

---

## 💡 Recommendations

### For Testing/Development:
1. **Start with Google Gemini** - Free tier available
2. Add OpenAI later for production use

### For Production:
1. **Use OpenAI GPT-4** - Best quality and reliability
2. Keep Gemini as backup option

### Budget-Conscious:
1. **Use Google Gemini** - Free tier
2. **Or Anthropic Claude** - Competitive pricing

---

## 🔒 Security Notes

1. **Never commit `.env` file to Git** (already in `.gitignore`)
2. **Never share your API keys publicly**
3. **Rotate keys if exposed**
4. **Use environment variables in production**

---

## 🚀 Next Steps

1. **Get at least ONE AI API key** (OpenAI, Claude, or Gemini)
2. Add it to your `.env` file
3. Run the app: `streamlit run app.py`
4. Start screening resumes!

---

## ❓ Need Help?

- **OpenAI**: https://help.openai.com
- **Anthropic**: https://docs.anthropic.com
- **Google AI**: https://ai.google.dev/docs
- **Supabase**: https://supabase.com/docs

