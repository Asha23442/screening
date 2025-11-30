"""
Quick start script for Resume Screening Agent
"""
import subprocess
import sys
import os

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("📝 Creating .env from env.example...")
        if os.path.exists('env.example'):
            with open('env.example', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✅ Created .env file. Please edit it with your API keys.")
            return False
        else:
            print("❌ env.example not found. Please create .env manually.")
            return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import langchain
        import chromadb
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False

def main():
    """Main function"""
    print("🚀 Starting Resume Screening Agent...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check .env file
    env_exists = check_env_file()
    if not env_exists:
        print("\n⚠️  Please configure your .env file before continuing.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    print("\n✅ Starting Streamlit app...")
    print("=" * 50)
    
    # Run streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

