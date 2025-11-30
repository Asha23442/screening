"""
Setup script for Resume Screening Agent
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resume-screening-agent",
    version="1.0.0",
    author="Resume Screening Agent",
    description="AI-powered resume screening and ranking system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.12.0",
        "anthropic>=0.18.1",
        "google-generativeai>=0.3.2",
        "langchain>=0.1.10",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-anthropic>=0.1.0",
        "langchain-google-genai>=0.0.6",
        "chromadb>=0.4.22",
        "streamlit>=1.31.1",
        "supabase>=2.3.0",
        "PyPDF2>=3.0.1",
        "python-docx>=1.1.0",
        "pdfplumber>=0.10.3",
        "python-dotenv>=1.0.1",
        "pandas>=2.2.0",
        "numpy>=1.26.3",
        "sentence-transformers>=2.3.1",
    ],
)

