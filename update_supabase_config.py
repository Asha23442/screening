"""
Update Supabase configuration in .env file
"""
import os
import re

def update_env_file():
    """Update Supabase credentials in .env file"""
    
    SUPABASE_URL = "https://kaodsueafxcnareczgni.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb2RzdWVhZnhjbmFyZWN6Z25pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzMDcyNDUsImV4cCI6MjA3OTg4MzI0NX0.ceSe_he6Rls6VjU069_OkUhSobRP87orYwJ9PnUmIYM"
    
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"[ERROR] {env_file} file not found!")
        print("Please create it from env.example first.")
        return False
    
    try:
        # Read existing .env file
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update SUPABASE_URL
        if re.search(r'^SUPABASE_URL=', content, re.MULTILINE):
            content = re.sub(
                r'^SUPABASE_URL=.*$',
                f'SUPABASE_URL={SUPABASE_URL}',
                content,
                flags=re.MULTILINE
            )
        else:
            # Add if not exists
            content += f'\nSUPABASE_URL={SUPABASE_URL}\n'
        
        # Update SUPABASE_KEY
        if re.search(r'^SUPABASE_KEY=', content, re.MULTILINE):
            content = re.sub(
                r'^SUPABASE_KEY=.*$',
                f'SUPABASE_KEY={SUPABASE_KEY}',
                content,
                flags=re.MULTILINE
            )
        else:
            # Add if not exists
            content += f'\nSUPABASE_KEY={SUPABASE_KEY}\n'
        
        # Write back
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Successfully updated {env_file} file!")
        print()
        print("Supabase credentials updated:")
        print(f"   SUPABASE_URL: {SUPABASE_URL}")
        print(f"   SUPABASE_KEY: {SUPABASE_KEY[:50]}...")
        print()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error updating .env file: {e}")
        return False

if __name__ == "__main__":
    update_env_file()

