"""
Supabase database integration
"""
import os
from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime
import json


class Database:
    """Supabase database operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            self.client = None
            print("Warning: Supabase credentials not found. Database features will be disabled.")
        else:
            try:
                self.client = create_client(supabase_url, supabase_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Supabase client: {e}")
                self.client = None
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.client is not None
    
    def test_connection(self) -> Dict[str, any]:
        """Test database connection and return status"""
        result = {
            "connected": False,
            "error": None,
            "tables_exist": False,
            "message": "",
            "tables_found": []
        }
        
        if not self.client:
            result["error"] = "Database client not initialized"
            result["message"] = "[ERROR] Please check SUPABASE_URL and SUPABASE_KEY in your .env file"
            return result
        
        try:
            # Try to query a simple table to test connection
            # First check if tables exist
            tables_to_check = ["job_descriptions", "resumes", "screening_results"]
            existing_tables = []
            
            for table in tables_to_check:
                try:
                    # Try to select from table (limit 0 to just test connection)
                    response = self.client.table(table).select("*").limit(0).execute()
                    # If we get here without exception, table exists
                    existing_tables.append(table)
                except Exception as table_error:
                    # Table might not exist or there's a permission issue
                    error_str = str(table_error).lower()
                    if "does not exist" in error_str or "relation" in error_str:
                        # Table doesn't exist, which is expected if not set up
                        pass
                    else:
                        # Other error (permission, etc.)
                        pass
            
            result["connected"] = True
            result["tables_exist"] = len(existing_tables) > 0
            result["tables_found"] = existing_tables
            
            if result["tables_exist"]:
                result["message"] = f"[OK] Connection successful! Found {len(existing_tables)}/{len(tables_to_check)} tables: {', '.join(existing_tables)}"
            else:
                result["message"] = f"[OK] Connection successful! However, no tables found. Please run the SQL setup script to create tables."
            
        except Exception as e:
            error_str = str(e)
            result["error"] = error_str
            result["message"] = f"[ERROR] Connection failed: {error_str}"
            
            # Provide helpful error messages
            if "Invalid API key" in error_str or "JWT" in error_str:
                result["message"] += "\n[TIP] Check your SUPABASE_KEY in .env file"
            elif "Invalid URL" in error_str or "url" in error_str.lower():
                result["message"] += "\n[TIP] Check your SUPABASE_URL in .env file"
            elif "permission" in error_str.lower():
                result["message"] += "\n[TIP] Check your API key permissions in Supabase"
        
        return result
    
    def create_tables(self):
        """Create necessary tables in Supabase (SQL to run in Supabase SQL editor)"""
        sql = """
        -- Create job_descriptions table
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            company TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Create resumes table
        CREATE TABLE IF NOT EXISTS resumes (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Create screening_results table
        CREATE TABLE IF NOT EXISTS screening_results (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            job_description_id UUID REFERENCES job_descriptions(id),
            resume_id UUID REFERENCES resumes(id),
            score FLOAT NOT NULL,
            model_used TEXT,
            analysis JSONB,
            matched_skills TEXT[],
            experience_years FLOAT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        return sql
    
    def save_job_description(self, title: str, description: str, company: str = None) -> Optional[str]:
        """Save job description to database"""
        if not self.is_connected():
            return None
        
        try:
            result = self.client.table("job_descriptions").insert({
                "title": title,
                "description": description,
                "company": company
            }).execute()
            
            if result.data:
                return result.data[0]['id']
        except Exception as e:
            print(f"Error saving job description: {e}")
        
        return None
    
    def save_resume(self, filename: str, content: str, email: str = None, phone: str = None) -> Optional[str]:
        """Save resume to database"""
        if not self.is_connected():
            return None
        
        try:
            result = self.client.table("resumes").insert({
                "filename": filename,
                "content": content,
                "email": email,
                "phone": phone
            }).execute()
            
            if result.data:
                return result.data[0]['id']
        except Exception as e:
            print(f"Error saving resume: {e}")
        
        return None
    
    def save_screening_result(self, job_id: str, resume_id: str, score: float, 
                             model_used: str, analysis: Dict, matched_skills: List[str] = None,
                             experience_years: float = None) -> Optional[str]:
        """Save screening result to database"""
        if not self.is_connected():
            return None
        
        try:
            result = self.client.table("screening_results").insert({
                "job_description_id": job_id,
                "resume_id": resume_id,
                "score": score,
                "model_used": model_used,
                "analysis": json.dumps(analysis),
                "matched_skills": matched_skills or [],
                "experience_years": experience_years
            }).execute()
            
            if result.data:
                return result.data[0]['id']
        except Exception as e:
            print(f"Error saving screening result: {e}")
        
        return None
    
    def get_screening_history(self, limit: int = 50) -> List[Dict]:
        """Get screening history"""
        if not self.is_connected():
            return []
        
        try:
            result = self.client.table("screening_results")\
                .select("*, job_descriptions(*), resumes(*)")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching screening history: {e}")
            return []

