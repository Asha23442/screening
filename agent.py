"""
Resume Screening Agent using LangChain and multiple AI models
"""
import os
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Use relative imports for better compatibility
try:
    from .vector_store import VectorStore
    from .utils import extract_skills, calculate_experience_years, clean_text
except ImportError:
    # Fallback for absolute imports
    from src.vector_store import VectorStore
    from src.utils import extract_skills, calculate_experience_years, clean_text


class ResumeScreeningAgent:
    """AI-powered resume screening agent"""
    
    def __init__(self, model_name: str = "openai"):
        """Initialize the agent with specified model"""
        self.model_name = model_name.lower()
        self.llm = self._initialize_model()
        self.vector_store = VectorStore()
    
    def _initialize_model(self):
        """Initialize the LLM based on model name"""
        if self.model_name == "openai" or self.model_name == "gpt":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.3
            )
        
        elif self.model_name == "claude" or self.model_name == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            return ChatAnthropic(
                model="claude-3-opus-20240229",
                temperature=0.3
            )
        
        elif self.model_name == "gemini" or self.model_name == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.3
            )
        
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
    
    def _create_screening_prompt(self, job_description: str, resume_text: str) -> str:
        """Create prompt for resume screening"""
        prompt = f"""You are an expert resume screening agent. Your task is to evaluate a resume against a job description and provide a comprehensive analysis.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Please provide a detailed analysis in the following JSON format:
{{
    "overall_score": <score from 0-100>,
    "strengths": ["strength1", "strength2", ...],
    "weaknesses": ["weakness1", "weakness2", ...],
    "matched_requirements": ["requirement1", "requirement2", ...],
    "missing_requirements": ["requirement1", "requirement2", ...],
    "recommendation": "HIRE" | "MAYBE" | "REJECT",
    "reasoning": "detailed explanation"
}}

Focus on:
1. Relevant experience and skills
2. Education and certifications
3. Cultural fit indicators
4. Career progression
5. Specific achievements and quantifiable results

Be thorough and objective in your evaluation."""
        
        return prompt
    
    def screen_resume(self, job_description: str, resume_text: str, 
                     resume_metadata: Dict = None) -> Dict:
        """Screen a single resume against job description"""
        # Clean texts
        job_description = clean_text(job_description)
        resume_text = clean_text(resume_text)
        
        # Calculate vector similarity
        vector_similarity = self.vector_store.calculate_similarity(
            job_description, resume_text
        )
        vector_score = vector_similarity * 100
        
        # Get AI analysis
        prompt = self._create_screening_prompt(job_description, resume_text)
        
        try:
            messages = [
                SystemMessage(content="You are an expert resume screening agent. Always respond with valid JSON."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            ai_analysis_text = response.content
            
            # Try to parse JSON from response
            import json
            import re
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', ai_analysis_text, re.DOTALL)
            if json_match:
                ai_analysis = json.loads(json_match.group())
            else:
                # Fallback if JSON parsing fails
                ai_analysis = {
                    "overall_score": vector_score,
                    "strengths": [],
                    "weaknesses": [],
                    "matched_requirements": [],
                    "missing_requirements": [],
                    "recommendation": "MAYBE",
                    "reasoning": ai_analysis_text
                }
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            ai_analysis = {
                "overall_score": vector_score,
                "strengths": [],
                "weaknesses": [],
                "matched_requirements": [],
                "missing_requirements": [],
                "recommendation": "MAYBE",
                "reasoning": f"AI analysis failed: {str(e)}"
            }
        
        # Extract additional information
        matched_skills = extract_skills(resume_text)
        experience_years = calculate_experience_years(resume_text)
        
        # Combine scores (weighted average: 70% AI, 30% vector similarity)
        final_score = (ai_analysis.get("overall_score", vector_score) * 0.7) + (vector_score * 0.3)
        
        # Build result
        result = {
            "score": round(final_score, 2),
            "vector_similarity": round(vector_similarity, 3),
            "ai_score": ai_analysis.get("overall_score", vector_score),
            "strengths": ai_analysis.get("strengths", []),
            "weaknesses": ai_analysis.get("weaknesses", []),
            "matched_requirements": ai_analysis.get("matched_requirements", []),
            "missing_requirements": ai_analysis.get("missing_requirements", []),
            "recommendation": ai_analysis.get("recommendation", "MAYBE"),
            "reasoning": ai_analysis.get("reasoning", ""),
            "matched_skills": matched_skills,
            "experience_years": experience_years,
            "model_used": self.model_name,
            "metadata": resume_metadata or {}
        }
        
        return result
    
    def screen_multiple_resumes(self, job_description: str, resumes: List[Dict]) -> List[Dict]:
        """Screen multiple resumes and rank them"""
        results = []
        
        # Add job description to vector store
        job_id = self.vector_store.add_job_description(
            job_description,
            {"timestamp": str(os.path.getmtime(__file__) if os.path.exists(__file__) else 0)}
        )
        
        for resume_data in resumes:
            resume_text = resume_data.get("text", "")
            resume_metadata = resume_data.get("metadata", {})
            
            # Add resume to vector store
            resume_id = self.vector_store.add_resume(resume_text, resume_metadata)
            
            # Screen resume
            result = self.screen_resume(job_description, resume_text, resume_metadata)
            result["resume_id"] = resume_id
            result["filename"] = resume_metadata.get("filename", "unknown")
            
            results.append(result)
        
        # Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Add rank
        for i, result in enumerate(results, 1):
            result["rank"] = i
        
        return results

