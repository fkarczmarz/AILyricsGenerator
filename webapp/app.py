import sys
import os

# Add the project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from webapp import app

if __name__ == '__main__':
    app.run(debug=True)