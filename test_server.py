"""
Test script for CV Digital Twin MCP Server
"""

import os
import sys
from pathlib import Path
import json

# Load .env file if it exists
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

# Import after setting environment
import main
from main import _chat_with_me_impl, load_all_pdfs_from_docs, find_all_pdfs_in_docs

def test_cv_loading():
    """Test CV loading functionality."""
    print("=" * 60)
    print("Testing PDF Loading")
    print("=" * 60)
    
    pdf_files = find_all_pdfs_in_docs()
    if pdf_files:
        print(f"✓ Found {len(pdf_files)} PDF file(s) in docs/ directory:")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file}")
        try:
            load_all_pdfs_from_docs()
            # Access the module's global variables
            import main
            cv_content = main.cv_content
            cv_metadata = main.cv_metadata
            print(f"✓ PDFs loaded successfully!")
            if cv_metadata.get("file_names"):
                print(f"  - Loaded files: {', '.join(cv_metadata['file_names'])}")
            print(f"  - Total content length: {len(cv_content)} characters")
            print(f"  - Preview (first 200 chars): {cv_content[:200]}...")
            return True
        except Exception as e:
            print(f"✗ Error loading PDFs: {e}")
            return False
    else:
        print("✗ No PDF files found in docs/ directory")
        return False


def test_chat():
    """Test chat functionality."""
    print("\n" + "=" * 60)
    print("Testing Chat Functionality")
    print("=" * 60)
    
    test_questions = [
        "Tell me about yourself",
        "What is your work experience?",
        "What are your skills?",
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 60)
        try:
            response = _chat_with_me_impl(question)
            result = json.loads(response)
            
            if "response" in result:
                print(f"Response: {result['response'][:200]}...")
                print(f"Model: {result.get('model', 'N/A')}")
            elif "status" in result and result["status"] == "error":
                print(f"Error: {result['message']}")
            else:
                print(f"Response: {response[:200]}...")
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Run all tests."""
    print("CV Digital Twin MCP Server - Local Test")
    print("=" * 60)
    
    # Test CV loading
    if not test_cv_loading():
        print("\n✗ CV loading failed. Cannot proceed with chat tests.")
        sys.exit(1)
    
    # Test chat
    test_chat()
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

