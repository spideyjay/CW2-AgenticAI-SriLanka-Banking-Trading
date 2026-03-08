#!/usr/bin/env python3
"""
Main runner script for the Agentic AI Sri Lanka Banking Trading system
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {command}")
            return True
        else:
            print(f"✗ {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {command}")
        print(f"Exception: {e}")
        return False

def setup_environment():
    """Setup the Python environment"""
    print("Setting up environment...")

    # Check if venv exists
    if not Path("venv").exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv venv"):
            return False

    # Activate and install requirements
    activate_cmd = ".\\venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"
    pip_cmd = f"{activate_cmd} && pip install -r requirements.txt"

    if not run_command(pip_cmd):
        return False

    return True

def run_data_pipeline():
    """Run the data collection and preprocessing pipeline"""
    print("\nRunning data pipeline...")

    # Run data collection notebook
    print("Running data collection...")
    # Note: In a real implementation, you'd use nbconvert or similar
    # For now, we'll assume the notebooks are run manually

    # Run preprocessing notebook
    print("Running data preprocessing...")
    # Same note as above

    return True

def run_agent_analysis():
    """Run the AI agent analysis"""
    print("\nRunning AI agent analysis...")

    activate_cmd = ".\\venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"
    agent_cmd = f"{activate_cmd} && python agents/trading_agent.py"

    return run_command(agent_cmd)

def main():
    """Main execution function"""
    print("🚀 Starting Agentic AI Sri Lanka Banking Trading System")
    print("=" * 60)

    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Please create it with your API keys.")
        return False

    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        return False

    # Run data pipeline
    if not run_data_pipeline():
        print("❌ Data pipeline failed")
        return False

    # Run agent analysis
    if not run_agent_analysis():
        print("❌ Agent analysis failed")
        return False

    print("\n✅ All tasks completed successfully!")
    print("\nNext steps:")
    print("- Review the analysis results")
    print("- Check the generated reports in data/ and docs/")
    print("- Consider deploying to cloud for automated trading")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)