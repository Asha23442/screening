# Database Setup Guide - Supabase

This guide will help you set up and connect to Supabase database for the Resume Screening Agent.

## 📋 Prerequisites

- A Supabase account (free tier is sufficient)
- Your project created in Supabase

## 🔑 Step 1: Get Your Supabase Credentials

1. **Go to Supabase Dashboard**
   - Visit https://supabase.com
   - Sign in or create an account

2. **Create or Select a Project**
   - Click "New Project" or select an existing one
   - Wait for the project to be fully provisioned (takes 1-2 minutes)

3. **Get API Credentials**
   - Go to **Settings** (gear icon) → **API**
   - You'll see two important values:
     - **Project URL**: Something like `https://xxxxx.supabase.co`
     - **API Keys**: 
       - `anon` `public` key (use this for client-side)
       - `service_role` `secret` key (use only for server-side, more powerful)

4. **Copy the Values**
   ```
   SUPABASE_URL = https://xxxxx.supabase.co
   SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (anon public key)
   ```

## ⚙️ Step 2: Configure Environment Variables

1. **Open your `.env` file** (create it from `env.example` if needed)

2. **Add your credentials**:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

3. **Save the file**

## 🗄️ Step 3: Create Database Tables

1. **Open SQL Editor**
   - In Supabase dashboard, click **SQL Editor** in the left sidebar
   - Click **New Query**

2. **Run the Setup SQL**
   - Copy the SQL from `src/database.py` (the `create_tables()` method)
   - Or use the SQL provided below:

```sql
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
```

3. **Execute the Query**
   - Click **Run** button (or press `Ctrl+Enter`)
   - You should see: "Success. No rows returned"

4. **Verify Tables Created**
   - Go to **Table Editor** in the left sidebar
   - You should see three tables:
     - `job_descriptions`
     - `resumes`
     - `screening_results`

## ✅ Step 4: Test the Connection

### Option 1: Using the Test Script
```bash
python test_database.py
```

### Option 2: Using the Streamlit App
1. Run the app: `streamlit run app.py`
2. Go to **Settings** tab
3. Click **Test Database Connection** button

### Option 3: Manual Test
```python
from src.database import Database

db = Database()
result = db.test_connection()
print(result)
```

## 🔒 Security Best Practices

1. **Use `anon` key for client-side** (what we're using)
   - Limited permissions, safe for client applications
   - Can be exposed in frontend code

2. **Use `service_role` key only for server-side**
   - Full access, bypasses Row Level Security
   - **NEVER expose in client-side code**

3. **Enable Row Level Security (RLS)** (Optional)
   - Go to **Authentication** → **Policies**
   - Create policies to restrict access if needed

## 🐛 Troubleshooting

### Error: "Invalid API key"
- **Solution**: Double-check your `SUPABASE_KEY` in `.env`
- Make sure there are no extra spaces or quotes
- Verify you're using the `anon` public key

### Error: "Invalid URL"
- **Solution**: Check your `SUPABASE_URL` format
- Should be: `https://xxxxx.supabase.co` (no trailing slash)
- Make sure it's the Project URL, not the API URL

### Error: "relation does not exist"
- **Solution**: Tables haven't been created yet
- Run the SQL setup script in Supabase SQL Editor
- Verify tables exist in Table Editor

### Error: "permission denied"
- **Solution**: Check your API key permissions
- Make sure you're using the correct key type
- Check if RLS policies are blocking access

### Connection works but can't insert data
- **Solution**: Check table permissions
- Verify your API key has INSERT permissions
- Check if RLS policies allow inserts

## 📊 Database Schema

### job_descriptions
- `id` (UUID, Primary Key)
- `title` (TEXT)
- `description` (TEXT)
- `company` (TEXT, nullable)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### resumes
- `id` (UUID, Primary Key)
- `filename` (TEXT)
- `content` (TEXT)
- `email` (TEXT, nullable)
- `phone` (TEXT, nullable)
- `created_at` (TIMESTAMP)

### screening_results
- `id` (UUID, Primary Key)
- `job_description_id` (UUID, Foreign Key → job_descriptions)
- `resume_id` (UUID, Foreign Key → resumes)
- `score` (FLOAT)
- `model_used` (TEXT)
- `analysis` (JSONB)
- `matched_skills` (TEXT[])
- `experience_years` (FLOAT)
- `created_at` (TIMESTAMP)

## 🔄 Resetting the Database

If you need to start fresh:

```sql
-- Drop tables (WARNING: This deletes all data!)
DROP TABLE IF EXISTS screening_results;
DROP TABLE IF EXISTS resumes;
DROP TABLE IF EXISTS job_descriptions;

-- Then run the create_tables() SQL again
```

## 📞 Need Help?

- Supabase Documentation: https://supabase.com/docs
- Supabase Discord: https://discord.supabase.com
- Check the test script output for detailed error messages

