"""
Database Connection Test Script
Run this script to test your Supabase database connection
"""
import os
from dotenv import load_dotenv
from src.database import Database

def main():
    """Test database connection"""
    print("=" * 60)
    print("Testing Supabase Database Connection")
    print("=" * 60)
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Check if environment variables are set
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("[ERROR] Supabase credentials not found!")
        print()
        print("Please set the following in your .env file:")
        print("  SUPABASE_URL=your_supabase_url")
        print("  SUPABASE_KEY=your_supabase_key")
        print()
        print("To get these values:")
        print("  1. Go to https://supabase.com")
        print("  2. Create or select a project")
        print("  3. Go to Settings > API")
        print("  4. Copy the 'Project URL' (SUPABASE_URL)")
        print("  5. Copy the 'anon' or 'service_role' key (SUPABASE_KEY)")
        return
    
    print(f"[OK] Found SUPABASE_URL: {supabase_url[:30]}...")
    print(f"[OK] Found SUPABASE_KEY: {supabase_key[:20]}...")
    print()
    
    # Initialize database
    print("Initializing database connection...")
    db = Database()
    
    # Test connection
    print("Testing connection...")
    result = db.test_connection()
    
    print()
    print("=" * 60)
    print("Connection Test Results")
    print("=" * 60)
    print()
    
    if result["connected"]:
        print(result["message"])
        print()
        
        if result["tables_exist"]:
            print("[OK] Database is ready to use!")
        else:
            print("[!] Tables not found. You need to create them.")
            print()
            print("To create tables:")
            print("  1. Go to your Supabase project")
            print("  2. Navigate to SQL Editor")
            print("  3. Run the following SQL:")
            print()
            print("-" * 60)
            sql_code = db.create_tables()
            print(sql_code)
            print("-" * 60)
    else:
        print(result["message"])
        if result["error"]:
            print(f"   Error details: {result['error']}")
        print()
        print("Troubleshooting:")
        print("  1. Verify your SUPABASE_URL is correct")
        print("  2. Verify your SUPABASE_KEY is correct")
        print("  3. Check if your Supabase project is active")
        print("  4. Ensure your IP is not blocked (if using IP restrictions)")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()

