#!/usr/bin/env python3
"""
IELTS Writing Feedback AI - Project Setup Script
Run this script to set up the complete project structure and dependencies
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run shell command and handle errors"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_backend():
    """Setup backend dependencies and environment"""
    print("\n🔧 Setting up Backend...")
    
    backend_dir = Path("backend")
    
    # Install UV if not available
    if run_command("which uv") is None:
        print("Installing UV package manager...")
        run_command("curl -LsSf https://astral.sh/uv/install.sh | sh")
    
    # Initialize UV project
    run_command("uv init", cwd=backend_dir)
    
    # Install dependencies
    deps = [
        "fastapi", "uvicorn[standard]", "sqlalchemy", "pydantic", "pydantic-settings",
        "python-multipart", "python-jose[cryptography]", "passlib[bcrypt]", "alembic",
        "langgraph", "langchain", "langchain-openai", "langchain-google-genai",
        "sslcommerz-python", "python-dotenv", "Pillow", "pytesseract"
    ]
    
    for dep in deps:
        run_command(f"uv add {dep}", cwd=backend_dir)
    
    # Create environment file
    if not (backend_dir / ".env").exists():
        print("📄 Creating .env file...")
        run_command("cp env.example .env", cwd=backend_dir)
        print("⚠️  Please edit backend/.env file with your actual API keys")

def setup_frontend():
    """Setup frontend dependencies"""
    print("\n🎨 Setting up Frontend...")
    
    frontend_dir = Path("frontend")
    
    # Check if already initialized
    if not (frontend_dir / "package.json").exists():
        print("❌ Frontend not initialized. Please run 'npm create vite@latest frontend -- --template react' first")
        return
    
    # Install dependencies
    run_command("npm install", cwd=frontend_dir)
    
    # Install additional packages
    additional_packages = [
        "axios", "react-router-dom", "lucide-react", "@headlessui/react", "@heroicons/react",
        "tailwindcss", "autoprefixer", "postcss"
    ]
    
    run_command(f"npm install {' '.join(additional_packages)}", cwd=frontend_dir)
    
    # Initialize Tailwind CSS
    run_command("npx tailwindcss init -p", cwd=frontend_dir)

def verify_installation():
    """Verify that everything is installed correctly"""
    print("\n🔍 Verifying Installation...")
    
    # Check backend
    backend_status = run_command("uv run python -c 'import fastapi; print(\"FastAPI OK\")'", cwd="backend")
    
    # Check frontend
    frontend_status = run_command("npm list react", cwd="frontend")
    
    if backend_status and frontend_status:
        print("✅ All dependencies installed successfully!")
        return True
    else:
        print("❌ Some dependencies failed to install")
        return False

def create_project_structure():
    """Ensure all directories exist"""
    print("\n📁 Creating project structure...")
    
    directories = [
        "backend/core", "backend/services", "backend/models", "backend/api", 
        "backend/database", "backend/tests",
        "frontend/src/components/Auth", "frontend/src/components/Payment",
        "frontend/src/components/Evaluation", "frontend/src/components/Dashboard",
        "frontend/src/components/Admin", "frontend/src/services", "frontend/src/pages",
        "frontend/src/hooks", "frontend/src/utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Project structure created!")

def show_next_steps():
    """Show next steps to the user"""
    print("\n🎉 Setup Complete! Next Steps:")
    print("\n1. Configure Environment:")
    print("   - Edit backend/.env with your API keys")
    print("   - Set OPENAI_API_KEY or GOOGLE_API_KEY")
    print("   - Configure SSLCommerz credentials")
    
    print("\n2. Start Development Servers:")
    print("   Backend:  cd backend && uv run uvicorn main:app --reload")
    print("   Frontend: cd frontend && npm run dev")
    
    print("\n3. Access Your Application:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    print("\n4. Initialize Database:")
    print("   cd backend && uv run python database/init_db.py")
    
    print("\n📚 Check README.md for detailed implementation guides!")

def main():
    """Main setup function"""
    print("🚀 IELTS Writing Feedback AI - Project Setup")
    print("=" * 50)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    create_project_structure()
    setup_backend()
    setup_frontend()
    
    if verify_installation():
        show_next_steps()
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
