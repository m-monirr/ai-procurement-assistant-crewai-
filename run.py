"""
Simple runner script for the research crew project.
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from research_crew.main import run

if __name__ == "__main__":
    run()
