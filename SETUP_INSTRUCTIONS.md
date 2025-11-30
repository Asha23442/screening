# Setup Instructions

## Quick Start

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**
   - Copy `env.example` to `.env`
   - Fill in your API keys:
     ```bash
     cp env.example .env
     # Edit .env with your API keys
     ```

3. **Required API Keys (Minimum)**
   - `OPENAI_API_KEY`: Get from https://platform.openai.com/api-keys
   - `SUPABASE_URL` and `SUPABASE_KEY`: Get from https://supabase.com

4. **Set Up Supabase Database**
   - Create a new project at https://supabase.com
   - Go to SQL Editor
   - Run the SQL from `src/database.py` (the `create_tables()` method output)

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Optional API Integrations

### Google Calendar
1. Go to Google Cloud Console
2. Create a service account
3. Download credentials JSON
4. Set `GOOGLE_CALENDAR_CREDENTIALS` path in `.env`

### Notion
1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the API key
4. Set `NOTION_API_KEY` in `.env`

### Google Sheets
1. Similar to Google Calendar setup
2. Enable Google Sheets API
3. Set `GOOGLE_SHEETS_CREDENTIALS` path in `.env`

## Troubleshooting

### Import Errors
If you encounter import errors, try:
```bash
pip install --upgrade langchain langchain-core langchain-openai
```

### ChromaDB Issues
If ChromaDB fails, it will create the database directory automatically. Make sure you have write permissions.

### API Key Issues
- Ensure your `.env` file is in the project root
- Check that API keys are correctly formatted (no extra spaces)
- Verify API keys are active and have sufficient credits

## Testing

To test the application:
1. Start the app: `streamlit run app.py`
2. Upload a sample job description
3. Upload one or more resume PDFs
4. Select an AI model
5. Click "Screen Resumes"

## Production Deployment

For production deployment:
1. Use environment variables from your hosting platform
2. Set up proper database backups
3. Configure rate limiting for API calls
4. Use a reverse proxy (nginx) if needed

