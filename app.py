"""
Resume Screening Agent - Streamlit Application
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Comprehensive path setup for Streamlit Cloud compatibility
current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent
grandparent_dir = parent_dir.parent

# Add all possible paths to sys.path
paths_to_add = [
    str(current_dir),
    str(parent_dir),
    str(grandparent_dir),
]

for path in paths_to_add:
    if path not in sys.path and Path(path).exists():
        sys.path.insert(0, path)

# Try to find src directory in multiple locations
possible_src_paths = [
    current_dir / "src",
    parent_dir / "src",
    grandparent_dir / "src",
    current_dir.parent.parent / "src",  # In case of nested structure
]

# Find and add src's parent directory to path
src_found = False
for src_path in possible_src_paths:
    if src_path.exists() and src_path.is_dir():
        parent_of_src = src_path.parent.absolute()
        parent_str = str(parent_of_src)
        if parent_str not in sys.path:
            sys.path.insert(0, parent_str)
        src_found = True
        break

# If src not found, try adding all parent directories up to 3 levels
if not src_found:
    for level in range(4):
        try_path = current_dir
        for _ in range(level):
            try_path = try_path.parent
        if (try_path / "src").exists():
            if str(try_path) not in sys.path:
                sys.path.insert(0, str(try_path))
            break

from dotenv import load_dotenv
import pandas as pd
from typing import List, Dict
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Import custom modules - Direct approach
# Handle both cases: files in src/ subdirectory OR files in same directory as app.py

def is_valid_src_dir(path):
    """Check if a path is a valid src directory with Python files"""
    if not path.exists() or not path.is_dir():
        return False
    # Check for required files
    required = ['agent.py', 'parsers.py', 'database.py']
    return all((path / f).exists() for f in required)

def has_required_files_in_dir(path):
    """Check if directory has required Python files directly in it"""
    if not path.exists() or not path.is_dir():
        return False
    required = ['agent.py', 'parsers.py', 'database.py']
    return all((path / f).exists() for f in required)

# First, check if files are in same directory as app.py (Streamlit Cloud case)
src_dir = None
use_src_prefix = True  # Default to using src prefix

if has_required_files_in_dir(current_dir):
    # Files are in the same directory as app.py
    src_dir = current_dir
    # We'll import directly without 'src.' prefix
    use_src_prefix = False
    # Add current directory to path
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
else:
    # Look for src/ subdirectory
    for possible_path in possible_src_paths:
        if is_valid_src_dir(possible_path):
            src_dir = possible_path
            break
    
    # If not found, search more thoroughly
    if not src_dir:
        for level in range(6):
            search_path = current_dir
            for _ in range(level):
                search_path = search_path.parent
            # Check if this directory has a src subdirectory
            test_src = search_path / "src"
            if is_valid_src_dir(test_src):
                src_dir = test_src
                if str(search_path) not in sys.path:
                    sys.path.insert(0, str(search_path))
                break
            # Also check if the search_path itself is the src directory (for nested repos)
            if is_valid_src_dir(search_path / "src" / "src"):
                src_dir = search_path / "src" / "src"
                if str(search_path / "src") not in sys.path:
                    sys.path.insert(0, str(search_path / "src"))
                break

# Ensure src's parent is in sys.path (unless src_dir is current_dir)
if src_dir and src_dir.exists() and src_dir != current_dir:
    parent_of_src = src_dir.parent.absolute()
    if str(parent_of_src) not in sys.path:
        sys.path.insert(0, str(parent_of_src))

# Try standard import first
try:
    if use_src_prefix:
        from src.agent import ResumeScreeningAgent
        from src.parsers import parse_resume, extract_resume_sections
        from src.database import Database
        from src.api_integrations import GoogleCalendarIntegration, NotionIntegration, GoogleSheetsIntegration
        from src.utils import export_to_json
    else:
        # Files are in same directory - import directly
        from agent import ResumeScreeningAgent
        from parsers import parse_resume, extract_resume_sections
        from database import Database
        from api_integrations import GoogleCalendarIntegration, NotionIntegration, GoogleSheetsIntegration
        from utils import export_to_json
except ImportError:
    # Fallback: Load modules directly using importlib
    if not src_dir or not src_dir.exists():
        st.error("❌ Could not find directory with required files.")
        st.error(f"**Current directory:** {current_dir}")
        st.error(f"**Parent directory:** {parent_dir}")
        st.error(f"**Searched paths:** {[str(p) for p in possible_src_paths]}")
        # Show what directories exist
        if current_dir.exists():
            st.error(f"**Files in current dir:** {[f.name for f in current_dir.iterdir() if f.is_file()][:10]}")
            st.error(f"**Dirs in current dir:** {[f.name for f in current_dir.iterdir() if f.is_dir()][:10]}")
        st.stop()
    
    # Verify src_dir has Python files
    py_files = list(src_dir.glob('*.py'))
    if not py_files:
        st.error(f"❌ Directory found but contains no Python files.")
        st.error(f"**Directory:** {src_dir}")
        st.error(f"**Contents:** {[f.name for f in src_dir.iterdir()]}")
        st.stop()
    
    import importlib.util
    import types
    
    # Determine module prefix based on whether we're using src/ or direct imports
    if use_src_prefix:
        # Create src package in sys.modules
        if 'src' not in sys.modules:
            src_package = types.ModuleType('src')
            src_package.__path__ = [str(src_dir)]
            sys.modules['src'] = src_package
        module_prefix = 'src.'
    else:
        # Files are in same directory - no prefix needed
        module_prefix = ''
    
    def load_module(name, filename):
        filepath = src_dir / filename
        if not filepath.exists():
            raise ImportError(f"File not found: {filepath}. Directory: {src_dir}, Files: {[f.name for f in src_dir.glob('*.py')]}")
        full_module_name = f'{module_prefix}{name}' if module_prefix else name
        spec = importlib.util.spec_from_file_location(full_module_name, filepath)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load: {filepath}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[full_module_name] = module
        spec.loader.exec_module(module)
        return module
    
    try:
        # Load in dependency order
        load_module('vector_store', 'vector_store.py')
        load_module('utils', 'utils.py')
        load_module('parsers', 'parsers.py')
        load_module('database', 'database.py')
        load_module('api_integrations', 'api_integrations.py')
        load_module('agent', 'agent.py')
        
        # Now import should work
        if use_src_prefix:
            from src.agent import ResumeScreeningAgent
            from src.parsers import parse_resume, extract_resume_sections
            from src.database import Database
            from src.api_integrations import GoogleCalendarIntegration, NotionIntegration, GoogleSheetsIntegration
            from src.utils import export_to_json
        else:
            from agent import ResumeScreeningAgent
            from parsers import parse_resume, extract_resume_sections
            from database import Database
            from api_integrations import GoogleCalendarIntegration, NotionIntegration, GoogleSheetsIntegration
            from utils import export_to_json
    except Exception as e:
        st.error("❌ Failed to load modules.")
        st.error(f"**Error:** {str(e)}")
        st.error(f"**Src directory:** {src_dir}")
        if src_dir and src_dir.exists():
            st.error(f"**Python files found:** {[f.name for f in src_dir.glob('*.py')]}")
            st.error(f"**All files:** {[f.name for f in src_dir.iterdir()]}")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="Resume Screening Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for responsive design
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .score-high {
        color: #4CAF50;
        font-size: 2rem;
        font-weight: bold;
    }
    .score-medium {
        color: #FF9800;
        font-size: 2rem;
        font-weight: bold;
    }
    .score-low {
        color: #f44336;
        font-size: 2rem;
        font-weight: bold;
    }
    .stExpander {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        .score-high, .score-medium, .score-low {
            font-size: 1.5rem;
        }
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'screening_results' not in st.session_state:
    st.session_state.screening_results = []
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'resumes' not in st.session_state:
    st.session_state.resumes = []


def main():
    """Main application"""
    st.title("📄 Resume Screening Agent")
    st.markdown("AI-powered resume screening and ranking system")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_option = st.selectbox(
            "Select AI Model",
            ["Gemini (Google)", "OpenAI GPT", "Claude (Anthropic)"],
            help="Choose the AI model for resume analysis"
        )
        
        # Map selection to model name
        model_map = {
            "OpenAI GPT": "openai",
            "Claude (Anthropic)": "claude",
            "Gemini (Google)": "gemini"
        }
        selected_model = model_map[model_option]
        
        st.divider()
        
        # Database status
        db = Database()
        if db.is_connected():
            # Test connection to show detailed status
            connection_test = db.test_connection()
            if connection_test["connected"]:
                st.success("✅ Supabase Connected")
                if connection_test["tables_exist"]:
                    st.caption("Database ready")
                else:
                    st.warning("⚠️ Tables not created")
                    if st.button("Show Setup SQL", key="show_sql_sidebar"):
                        st.code(db.create_tables(), language="sql")
            else:
                st.error("❌ Connection Failed")
                st.caption(connection_test.get("message", "Check your credentials"))
        else:
            st.warning("⚠️ Supabase Not Connected")
            st.caption("Database features will be disabled")
            if st.button("Test Connection", key="test_conn_sidebar"):
                with st.spinner("Testing..."):
                    test_result = db.test_connection()
                    if test_result["connected"]:
                        st.success(test_result["message"])
                    else:
                        st.error(test_result["message"])
        
        st.divider()
        
        # API Integrations status
        st.subheader("API Integrations")
        cal_integration = GoogleCalendarIntegration()
        notion_integration = NotionIntegration()
        sheets_integration = GoogleSheetsIntegration()
        
        if cal_integration.service:
            st.success("✅ Google Calendar")
        else:
            st.info("ℹ️ Google Calendar (Optional)")
        
        if notion_integration.client:
            st.success("✅ Notion")
        else:
            st.info("ℹ️ Notion (Optional)")
        
        if sheets_integration.client:
            st.success("✅ Google Sheets")
        else:
            st.info("ℹ️ Google Sheets (Optional)")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Screen Resumes", "📊 Results", "📈 History", "⚙️ Settings"])
    
    with tab1:
        screen_resumes_tab(selected_model, db)
    
    with tab2:
        results_tab()
    
    with tab3:
        history_tab(db)
    
    with tab4:
        settings_tab()


def screen_resumes_tab(model_name: str, db: Database):
    """Screen resumes tab"""
    st.header("Screen Resumes")
    
    # Check API key for selected model
    model_key_map = {
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "gemini": "GOOGLE_API_KEY"
    }
    
    required_key = model_key_map.get(model_name)
    if required_key and not os.getenv(required_key):
        st.error(f"⚠️ {required_key} not found in environment variables. Please add it to your .env file.")
        st.info("The application will not work without the required API key.")
        return
    
    # Job description input
    st.subheader("Job Description")
    job_description_input = st.text_area(
        "Enter or paste job description",
        height=200,
        value=st.session_state.job_description,
        help="Paste the complete job description here"
    )
    
    if job_description_input:
        st.session_state.job_description = job_description_input
    
    st.divider()
    
    # Resume upload
    st.subheader("Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload resume files (PDF or DOCX)",
        type=['pdf', 'docx', 'doc'],
        accept_multiple_files=True,
        help="Upload one or multiple resume files"
    )
    
    if uploaded_files:
        st.session_state.resumes = []
        for uploaded_file in uploaded_files:
            try:
                file_content = uploaded_file.read()
                resume_text = parse_resume(file_content, uploaded_file.name)
                resume_sections = extract_resume_sections(resume_text)
                
                st.session_state.resumes.append({
                    "text": resume_text,
                    "metadata": {
                        "filename": uploaded_file.name,
                        "name": resume_sections.get("name", ""),
                        "email": resume_sections.get("email", ""),
                        "phone": resume_sections.get("phone", ""),
                        "sections": resume_sections
                    }
                })
                
                st.success(f"✅ {uploaded_file.name} parsed successfully")
            except Exception as e:
                st.error(f"❌ Error parsing {uploaded_file.name}: {str(e)}")
    
    st.divider()
    
    # Screen button
    if st.button("🔍 Screen Resumes", type="primary", use_container_width=True):
        if not st.session_state.job_description:
            st.error("Please enter a job description")
        elif not st.session_state.resumes:
            st.error("Please upload at least one resume")
        else:
            with st.spinner("Screening resumes... This may take a few moments."):
                try:
                    agent = ResumeScreeningAgent(model_name=model_name)
                    results = agent.screen_multiple_resumes(
                        st.session_state.job_description,
                        st.session_state.resumes
                    )
                    
                    st.session_state.screening_results = results
                    
                    # Save to database if connected
                    if db.is_connected():
                        job_id = db.save_job_description(
                            title="Job Position",
                            description=st.session_state.job_description
                        )
                        
                        for result in results:
                            resume_id = db.save_resume(
                                filename=result.get("filename", "unknown"),
                                content=st.session_state.resumes[result.get("rank", 1) - 1]["text"],
                                email=result.get("metadata", {}).get("email"),
                                phone=result.get("metadata", {}).get("phone")
                            )
                            
                            if job_id and resume_id:
                                db.save_screening_result(
                                    job_id=job_id,
                                    resume_id=resume_id,
                                    score=result.get("score", 0),
                                    model_used=model_name,
                                    analysis=result,
                                    matched_skills=result.get("matched_skills", []),
                                    experience_years=result.get("experience_years", 0)
                                )
                    
                    st.success(f"✅ Successfully screened {len(results)} resumes!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error during screening: {str(e)}")
                    st.info("Please check your API keys in the .env file")


def results_tab():
    """Results display tab"""
    st.header("Screening Results")
    
    if not st.session_state.screening_results:
        st.info("No screening results yet. Please screen some resumes first.")
        return
    
    results = st.session_state.screening_results
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Resumes", len(results))
    
    with col2:
        avg_score = sum(r.get("score", 0) for r in results) / len(results)
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    with col3:
        top_candidates = len([r for r in results if r.get("recommendation") == "HIRE"])
        st.metric("Top Candidates", top_candidates)
    
    with col4:
        st.metric("Model Used", results[0].get("model_used", "unknown").upper())
    
    st.divider()
    
    # Results table
    st.subheader("Ranked Results")
    
    # Create DataFrame for display
    df_data = []
    for result in results:
        df_data.append({
            "Rank": result.get("rank", 0),
            "Filename": result.get("filename", "unknown"),
            "Score": f"{result.get('score', 0):.1f}%",
            "Recommendation": result.get("recommendation", "MAYBE"),
            "Experience": f"{result.get('experience_years', 0):.1f} years",
            "Skills": len(result.get("matched_skills", []))
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Detailed view
    st.subheader("Detailed Analysis")
    
    for result in results:
        with st.expander(f"Rank #{result.get('rank')}: {result.get('filename')} - Score: {result.get('score'):.1f}%"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Scores")
                score = result.get("score", 0)
                if score >= 80:
                    st.markdown(f'<p class="score-high">{score:.1f}%</p>', unsafe_allow_html=True)
                elif score >= 60:
                    st.markdown(f'<p class="score-medium">{score:.1f}%</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="score-low">{score:.1f}%</p>', unsafe_allow_html=True)
                
                st.metric("AI Score", f"{result.get('ai_score', 0):.1f}%")
                st.metric("Vector Similarity", f"{result.get('vector_similarity', 0):.3f}")
                st.metric("Experience", f"{result.get('experience_years', 0):.1f} years")
            
            with col2:
                st.markdown("### ✅ Strengths")
                for strength in result.get("strengths", []):
                    st.success(f"• {strength}")
                
                st.markdown("### ⚠️ Weaknesses")
                for weakness in result.get("weaknesses", []):
                    st.warning(f"• {weakness}")
            
            st.markdown("### 🎯 Matched Requirements")
            for req in result.get("matched_requirements", []):
                st.info(f"✓ {req}")
            
            st.markdown("### ❌ Missing Requirements")
            for req in result.get("missing_requirements", []):
                st.error(f"✗ {req}")
            
            st.markdown("### 💡 Skills")
            skills = result.get("matched_skills", [])
            if skills:
                st.write(", ".join(skills))
            else:
                st.write("No skills detected")
            
            st.markdown("### 📝 Reasoning")
            st.write(result.get("reasoning", "No reasoning provided"))
    
    st.divider()
    
    # Export options
    st.subheader("Export Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export to CSV"):
            df_export = pd.DataFrame(st.session_state.screening_results)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"resume_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📄 Export to JSON"):
            json_data = json.dumps(st.session_state.screening_results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"resume_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        sheets_integration = GoogleSheetsIntegration()
        if sheets_integration.client:
            spreadsheet_id = st.text_input("Google Sheets ID", placeholder="Enter spreadsheet ID")
            if st.button("📊 Export to Google Sheets"):
                if spreadsheet_id:
                    if sheets_integration.export_results(spreadsheet_id, st.session_state.screening_results):
                        st.success("✅ Exported to Google Sheets!")
                    else:
                        st.error("❌ Failed to export")
                else:
                    st.warning("Please enter a spreadsheet ID")


def history_tab(db: Database):
    """History tab"""
    st.header("Screening History")
    
    if not db.is_connected():
        st.warning("Supabase is not connected. History features are unavailable.")
        st.info("To enable history, configure SUPABASE_URL and SUPABASE_KEY in your .env file")
        return
    
    history = db.get_screening_history(limit=50)
    
    if not history:
        st.info("No screening history found.")
        return
    
    st.subheader(f"Recent Screenings ({len(history)} results)")
    
    for item in history:
        with st.expander(f"Screening on {item.get('created_at', 'Unknown date')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Job Description:**")
                job_desc = item.get('job_descriptions', {})
                st.write(f"Title: {job_desc.get('title', 'N/A')}")
                st.write(f"Company: {job_desc.get('company', 'N/A')}")
            
            with col2:
                st.write("**Resume:**")
                resume = item.get('resumes', {})
                st.write(f"Filename: {resume.get('filename', 'N/A')}")
                st.write(f"Email: {resume.get('email', 'N/A')}")
            
            st.write(f"**Score:** {item.get('score', 0):.1f}%")
            st.write(f"**Model:** {item.get('model_used', 'N/A')}")


def settings_tab():
    """Settings tab"""
    st.header("Settings & Configuration")
    
    st.subheader("API Keys Configuration")
    st.info("Configure your API keys in the .env file. See .env.example for reference.")
    
    st.markdown("""
    ### Required API Keys:
    - **OPENAI_API_KEY**: For OpenAI GPT models
    - **SUPABASE_URL** and **SUPABASE_KEY**: For database features
    
    ### Optional API Keys:
    - **ANTHROPIC_API_KEY**: For Claude models
    - **GOOGLE_API_KEY**: For Gemini models
    - **NOTION_API_KEY**: For Notion integration
    - **GOOGLE_CALENDAR_CREDENTIALS**: Path to Google Calendar credentials JSON
    - **GOOGLE_SHEETS_CREDENTIALS**: Path to Google Sheets credentials JSON
    """)
    
    st.divider()
    
    st.subheader("Database Connection")
    
    # Test connection button
    db = Database()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Test Database Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                test_result = db.test_connection()
                
                if test_result["connected"]:
                    st.success(test_result["message"])
                    if test_result["tables_exist"]:
                        st.balloons()
                else:
                    st.error(test_result["message"])
                    if test_result.get("error"):
                        st.code(test_result["error"], language="text")
    
    with col2:
        if st.button("📋 Copy Setup Instructions", use_container_width=True):
            st.info("Instructions copied to clipboard (see below)")
    
    st.divider()
    
    st.subheader("Database Setup")
    
    st.markdown("""
    ### Step 1: Get Your Supabase Credentials
    
    1. Go to [Supabase](https://supabase.com) and create/login to your account
    2. Create a new project or select an existing one
    3. Navigate to **Settings** → **API**
    4. Copy the following:
       - **Project URL** → This is your `SUPABASE_URL`
       - **anon public** key → This is your `SUPABASE_KEY` (use anon key for client-side)
    
    ### Step 2: Add to .env File
    
    Add these lines to your `.env` file:
    ```env
    SUPABASE_URL=https://your-project.supabase.co
    SUPABASE_KEY=your-anon-key-here
    ```
    
    ### Step 3: Create Database Tables
    
    Run the following SQL in your Supabase SQL Editor:
    """)
    
    sql_code = db.create_tables()
    st.code(sql_code, language="sql")
    
    st.markdown("""
    **How to run SQL:**
    1. In Supabase dashboard, go to **SQL Editor**
    2. Click **New Query**
    3. Paste the SQL above
    4. Click **Run** (or press Ctrl+Enter)
    5. You should see "Success. No rows returned"
    
    ### Step 4: Verify Connection
    
    Click the "Test Database Connection" button above to verify everything is working.
    """)
    
    st.divider()
    
    # Show current connection status
    st.subheader("Current Connection Status")
    if db.is_connected():
        test_result = db.test_connection()
        if test_result["connected"]:
            st.success(f"✅ {test_result['message']}")
        else:
            st.error(f"❌ {test_result['message']}")
    else:
        st.warning("⚠️ Database not configured. Please add SUPABASE_URL and SUPABASE_KEY to your .env file.")
    
    st.divider()
    
    st.subheader("About")
    st.markdown("""
    **Resume Screening Agent** v1.0
    
    Built with:
    - LangChain for AI orchestration
    - ChromaDB for vector storage
    - Supabase for database
    - Streamlit for UI
    
    Supports multiple AI models: OpenAI GPT, Claude, and Gemini
    """)


if __name__ == "__main__":
    main()

