"""
Superstore Sales Dashboard
Main entry point - runs the Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Run the dashboard"""
    print("=" * 60)
    print("📊 SUPERSTORE SALES DASHBOARD")
    print("=" * 60)
    print("\n🚀 Starting your dashboard...")
    print("\n📂 Loading data from: SALES_DATA_SETT.xlsx")
    print("🔄 Starting Streamlit server...")
    print("\n📍 Dashboard will open in your browser automatically")
    print("📍 URL: http://localhost:8501")
    print("📍 Press Ctrl+C in this terminal to stop")
    print("=" * 60)
    
    # Check if data file exists
    if not os.path.exists('SALES_DATA_SETT.xlsx'):
        print("\n❌ ERROR: SALES_DATA_SETT.xlsx not found!")
        print("Please make sure the Excel file is in the same folder as main.py")
        return
    
    # Check if other required files exist
    required_files = ['analysis.py', 'dashboard.py', 'streamlit_app.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"\n❌ ERROR: Missing files: {', '.join(missing_files)}")
        print("Please make sure all required files are present")
        return
    
    print("\n✅ All files found! Launching dashboard...\n")
    
    # Run streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
