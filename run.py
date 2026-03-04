"""
SUCHANA HUB - Application Entry Point
Main script to run the Flask application

To run this application:
1. Set up PostgreSQL database
2. Create Python virtual environment
3. Install dependencies: pip install -r requirements.txt
4. Run: python run.py

This creates the Flask app and starts the development server
"""

import os
import webbrowser
import threading
import time
from app import create_app
from config import Config, DevelopmentConfig, ProductionConfig

# Determine which configuration to use based on environment variable
# Default to development if not specified
environment = os.environ.get('FLASK_ENV', 'development')

if environment == 'production':
    config = ProductionConfig()
elif environment == 'testing':
    config = DevelopmentConfig()
else:
    config = DevelopmentConfig()

# Create Flask application using factory
app = create_app(config)

def open_browser():
    """Open login page in default browser after server starts"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://127.0.0.1:5000/login')

if __name__ == '__main__':
    """
    Run Flask development server
    
    Parameters:
    - debug=True: Enables auto-reload on code changes and interactive debugger
    - host='0.0.0.0': Listen on all network interfaces
    - port=5000: Run on port 5000
    - use_reloader=True: Auto-reload on file changes
    """
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║        SUCHANA HUB - Attendance & Notification System     ║
    ║                                                            ║
    ║  🎓 A Smart College Attendance & Guardian Notification    ║
    ║     System - MCA Semester Project                          ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    
    📝 Application Details:
    - Environment: {}
    - Database: PostgreSQL
    - Framework: Flask + SQLAlchemy
    
    🚀 Server Starting...
    - URL: http://localhost:5000
    - Debug Mode: {}
    
    📚 Default Login Credentials:
    - Admin: admin / admin123
    - Teacher: teacher / teacher123  
    - Staff: staff / staff123
    
    (Change these credentials in production!)
    
    ⚠️  Press CTRL+C to stop the server
    """.format(environment.upper(), app.debug))
    
    # Start browser opener in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )
