# tests/conftest.py
import sys
import os

# Add the parent directory to the path so pytest can find the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
