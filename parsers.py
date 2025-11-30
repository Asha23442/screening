"""
PDF and DOCX parsing utilities
"""
import PyPDF2
import pdfplumber
from docx import Document
from typing import Optional
import io


def parse_pdf(file_content: bytes) -> str:
    """Parse PDF file and extract text"""
    text = ""
    
    # Try pdfplumber first (better for complex PDFs)
    try:
        pdf_file = io.BytesIO(file_content)
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        # Fallback to PyPDF2
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e2:
            raise Exception(f"Failed to parse PDF: {str(e2)}")
    
    return text.strip()


def parse_docx(file_content: bytes) -> str:
    """Parse DOCX file and extract text"""
    try:
        doc_file = io.BytesIO(file_content)
        doc = Document(doc_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to parse DOCX: {str(e)}")


def parse_resume(file_content: bytes, filename: str) -> str:
    """Parse resume file based on extension"""
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return parse_pdf(file_content)
    elif filename_lower.endswith('.docx') or filename_lower.endswith('.doc'):
        return parse_docx(file_content)
    else:
        raise ValueError(f"Unsupported file format: {filename}. Supported: PDF, DOCX")


def extract_resume_sections(text: str) -> dict:
    """Extract structured sections from resume text"""
    sections = {
        'name': '',
        'email': '',
        'phone': '',
        'summary': '',
        'experience': '',
        'education': '',
        'skills': '',
        'full_text': text
    }
    
    # Extract email
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        sections['email'] = emails[0]
    
    # Extract phone
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        sections['phone'] = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
    
    # Try to identify sections (basic approach)
    text_lower = text.lower()
    lines = text.split('\n')
    
    # Look for common section headers
    section_keywords = {
        'summary': ['summary', 'objective', 'profile', 'about'],
        'experience': ['experience', 'employment', 'work history', 'professional experience'],
        'education': ['education', 'academic', 'qualifications'],
        'skills': ['skills', 'technical skills', 'competencies']
    }
    
    current_section = None
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        for section, keywords in section_keywords.items():
            if any(keyword in line_lower for keyword in keywords) and len(line) < 50:
                current_section = section
                break
        
        if current_section and current_section in sections:
            if sections[current_section]:
                sections[current_section] += '\n' + line
            else:
                sections[current_section] = line
    
    return sections

