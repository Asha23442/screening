# Resume Screening Agent

An intelligent AI-powered resume screening system that ranks resumes based on job descriptions using multiple AI models and vector databases.

## Features

- 🤖 **Multi-Model Support**: OpenAI GPT, Claude (Anthropic), and Google Gemini
- 📊 **Vector Database**: ChromaDB for semantic search and similarity matching
- 🎯 **Intelligent Ranking**: Advanced scoring system based on job requirements
- 💾 **Database Integration**: Supabase for storing results and history
- 📅 **API Integrations**: Google Calendar, Notion, Google Sheets
- 🎨 **Responsive UI**: Modern Streamlit interface
- 📄 **Multi-Format Support**: PDF, DOCX resume parsing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your API keys
```

4. Run the application:
```bash
# Option 1: Use the quick start script
python run.py

# Option 2: Run directly with Streamlit
streamlit run app.py
```

## Configuration

### Required API Keys:
- **OpenAI API Key**: Get from https://platform.openai.com/api-keys
- **Supabase**: Get from https://supabase.com
  - See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed setup instructions
  - Test connection: `python test_database.py`

### Optional API Keys:
- **Anthropic API Key**: For Claude model
- **Google API Key**: For Gemini model
- **Notion API Key**: For Notion integration
- **Google Calendar/Sheets**: For calendar and sheets integration

## Usage

1. **Upload Job Description**: Paste or upload a job description
2. **Upload Resumes**: Upload one or multiple resume files (PDF/DOCX)
3. **Select AI Model**: Choose from OpenAI, Claude, or Gemini
4. **Screen Resumes**: Click "Screen Resumes" to get ranked results
5. **View Results**: See ranked resumes with scores and detailed analysis
6. **Export Results**: Export to CSV or save to Supabase

## Project Structure

```
ai/
├── app.py                 # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── agent.py          # Resume screening agent
│   ├── vector_store.py   # Vector database operations
│   ├── database.py       # Supabase integration
│   ├── parsers.py        # PDF/DOCX parsing
│   ├── api_integrations.py  # External API integrations
│   └── utils.py          # Utility functions
├── requirements.txt
├── env.example
├── run.py              # Quick start script
├── setup.py            # Package setup
└── README.md
```
```

## Technologies Used

- **AI Models**: OpenAI GPT-4, Claude, Gemini
- **Frameworks**: LangChain, CrewAI
- **Vector DB**: ChromaDB
- **Database**: Supabase
- **UI**: Streamlit
- **APIs**: Google Calendar, Notion, Google Sheets

## License

MIT License

