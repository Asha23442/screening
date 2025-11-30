"""
Utility functions for resume screening
"""
import re
import json
from typing import List, Dict, Any
from datetime import datetime


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-]', '', text)
    return text.strip()


def extract_skills(text: str) -> List[str]:
    """Extract skills from text"""
    common_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
        'AWS', 'Docker', 'Kubernetes', 'Git', 'Machine Learning', 'AI',
        'TensorFlow', 'PyTorch', 'Data Science', 'Analytics', 'Agile', 'Scrum'
    ]
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills


def calculate_experience_years(text: str) -> float:
    """Calculate years of experience from resume text"""
    # Look for patterns like "5 years", "3+ years", etc.
    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?',
    ]
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            try:
                years.append(float(match))
            except:
                pass
    
    if years:
        return max(years)
    return 0.0


def format_score(score: float) -> str:
    """Format score as percentage"""
    return f"{score:.1f}%"


def create_summary(data: Dict[str, Any]) -> str:
    """Create a summary from screening data"""
    summary = f"""
    **Match Score**: {data.get('score', 0):.1f}%
    **Experience**: {data.get('experience_years', 0):.1f} years
    **Skills Match**: {len(data.get('matched_skills', []))} skills
    **Education**: {data.get('education', 'Not specified')}
    """
    return summary.strip()


def export_to_json(data: List[Dict], filename: str = None):
    """Export data to JSON"""
    if filename is None:
        filename = f"resume_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filename

