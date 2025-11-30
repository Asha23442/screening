"""
Quick setup script to create .env file with Supabase credentials
"""
import os

def create_env_file():
    """Create .env file with Supabase credentials"""
    
    # Your Supabase credentials
    SUPABASE_URL = "https://kaodsueafxcnareczgni.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb2RzdWVhZnhjbmFyZWN6Z25pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzMDcyNDUsImV4cCI6MjA3OTg4MzI0NX0.ceSe_he6Rls6VjU069_OkUhSobRP87orYwJ9PnUmIYM"
    
    env_content = f"""# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Claude) API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Supabase Configuration
SUPABASE_URL={SUPABASE_URL}
SUPABASE_KEY={SUPABASE_KEY}

# Google Calendar API (Optional)
GOOGLE_CALENDAR_CREDENTIALS=path_to_credentials_json

# Notion API (Optional)
NOTION_API_KEY=your_notion_api_key_here

# Google Sheets API (Optional)
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials_json

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
"""
    
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"[!] {env_file} already exists!")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"[OK] Successfully created {env_file} file!")
        print()
        print("Your Supabase credentials have been added:")
        print(f"   SUPABASE_URL: {SUPABASE_URL}")
        print(f"   SUPABASE_KEY: {SUPABASE_KEY[:50]}...")
        print()
        print("[!] IMPORTANT: Add your OpenAI API key to use the app!")
        print("   Edit .env and add: OPENAI_API_KEY=your_key_here")
        print()
        print("To test the database connection, run:")
        print("   python test_database.py")
    except Exception as e:
        print(f"[ERROR] Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()

