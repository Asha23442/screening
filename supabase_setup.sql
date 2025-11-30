-- Resume Screening Agent - Supabase Database Setup
-- Copy and paste this entire file into Supabase SQL Editor

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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_screening_results_job_id ON screening_results(job_description_id);
CREATE INDEX IF NOT EXISTS idx_screening_results_resume_id ON screening_results(resume_id);
CREATE INDEX IF NOT EXISTS idx_screening_results_score ON screening_results(score DESC);
CREATE INDEX IF NOT EXISTS idx_screening_results_created_at ON screening_results(created_at DESC);

-- Success message (this won't execute, just for reference)
-- After running this script, you should see: "Success. No rows returned"

