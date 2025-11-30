# Resume Screening Agent - Project Overview

## 🎯 Project Description

A fully functional, AI-powered resume screening system that automatically ranks and evaluates resumes against job descriptions. The system uses multiple AI models, vector databases, and integrates with various external services to provide a comprehensive hiring solution.

## ✨ Key Features

### 1. Multi-Model AI Support
- **OpenAI GPT-4**: High-quality analysis with deep understanding
- **Claude (Anthropic)**: Advanced reasoning capabilities
- **Google Gemini**: Cost-effective alternative with good performance

### 2. Intelligent Ranking System
- Combines AI analysis (70%) with vector similarity (30%)
- Provides detailed scoring with strengths, weaknesses, and recommendations
- Matches skills, experience, and requirements automatically

### 3. Vector Database (ChromaDB)
- Semantic search for finding similar resumes
- Stores job descriptions and resumes for future reference
- Cosine similarity matching for accurate comparisons

### 4. Database Integration (Supabase)
- Stores all screening results
- Maintains history of past screenings
- Tracks job descriptions and resumes

### 5. API Integrations
- **Google Calendar**: Schedule interviews automatically
- **Notion**: Create candidate pages in your workspace
- **Google Sheets**: Export results to spreadsheets

### 6. Responsive UI (Streamlit)
- Modern, clean interface
- Mobile-friendly design
- Real-time results display
- Export capabilities (CSV, JSON)

### 7. Document Parsing
- PDF parsing (PyPDF2, pdfplumber)
- DOCX parsing (python-docx)
- Automatic section extraction (name, email, skills, etc.)

## 📁 Project Structure

```
ai/
├── app.py                      # Main Streamlit application
├── run.py                      # Quick start script
├── setup.py                    # Package setup
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Main documentation
├── SETUP_INSTRUCTIONS.md       # Detailed setup guide
├── PROJECT_OVERVIEW.md         # This file
└── src/
    ├── __init__.py
    ├── agent.py                # Core screening agent (LangChain)
    ├── vector_store.py         # ChromaDB operations
    ├── database.py             # Supabase integration
    ├── parsers.py              # PDF/DOCX parsing
    ├── api_integrations.py     # External API clients
    └── utils.py                # Utility functions
```

## 🔧 Technical Stack

### AI & ML
- **LangChain**: AI orchestration and prompt management
- **OpenAI**: GPT-4 Turbo for resume analysis
- **Anthropic**: Claude for alternative analysis
- **Google**: Gemini for cost-effective analysis
- **Sentence Transformers**: Embedding generation

### Data Storage
- **ChromaDB**: Vector database for semantic search
- **Supabase**: PostgreSQL database for structured data

### UI & Framework
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and export

### Document Processing
- **PyPDF2**: PDF parsing
- **pdfplumber**: Advanced PDF extraction
- **python-docx**: Word document parsing

### Integrations
- **Google APIs**: Calendar and Sheets
- **Notion API**: Workspace integration

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Set Up Supabase** (Optional but recommended)
   - Create project at https://supabase.com
   - Run SQL from `src/database.py` in SQL Editor

4. **Run Application**
   ```bash
   python run.py
   # or
   streamlit run app.py
   ```

## 📊 Workflow

1. **Input Phase**
   - User enters job description
   - User uploads one or more resumes (PDF/DOCX)

2. **Processing Phase**
   - Resumes are parsed and text extracted
   - Job description and resumes are embedded
   - Vector similarity is calculated
   - AI model analyzes each resume

3. **Analysis Phase**
   - Scores are calculated (weighted combination)
   - Strengths and weaknesses identified
   - Requirements matched/missing
   - Recommendations generated

4. **Output Phase**
   - Results ranked by score
   - Detailed analysis displayed
   - Results saved to database
   - Export options available

## 🎨 UI Features

### Main Tabs
1. **Screen Resumes**: Upload and screen resumes
2. **Results**: View detailed rankings and analysis
3. **History**: Browse past screening sessions
4. **Settings**: Configuration and setup instructions

### Responsive Design
- Works on desktop, tablet, and mobile
- Adaptive layouts for different screen sizes
- Touch-friendly interface

## 🔐 Security & Privacy

- API keys stored in environment variables
- No hardcoded credentials
- Local vector database (ChromaDB)
- Optional cloud database (Supabase)

## 📈 Future Enhancements

Potential improvements:
- Batch processing for large volumes
- Custom scoring weights
- Multi-language support
- Advanced filtering options
- Email notifications
- Interview scheduling automation
- ATS integration

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Solution: `pip install --upgrade langchain langchain-core`

2. **API Key Errors**
   - Check .env file exists and has correct keys
   - Verify keys are active and have credits

3. **ChromaDB Errors**
   - Ensure write permissions in project directory
   - Check disk space availability

4. **PDF Parsing Issues**
   - Try different PDF files
   - Ensure PDFs are not password-protected
   - Check file format compatibility

## 📝 License

MIT License - See LICENSE file for details

## 👥 Contributing

This is a complete, production-ready project. Feel free to:
- Fork and modify for your needs
- Report issues
- Suggest improvements
- Add new features

## 🙏 Acknowledgments

Built with:
- LangChain community
- Streamlit team
- ChromaDB developers
- Supabase team

---

**Status**: ✅ Fully Functional
**Version**: 1.0.0
**Last Updated**: 2024

