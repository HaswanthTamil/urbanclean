import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.server import app, generate_map

if __name__ == "__main__":
    generate_map()
    app.run(debug=True, port=5000)
