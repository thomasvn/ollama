#!/usr/bin/env python3

"""
Setup Instructions:
1. Create and activate venv: python3 -m venv venv && source venv/bin/activate
2. Install packages: pip3 install requests
3. Start Ollama: docker run -d -p 11434:11434 ollama/ollama
"""

import requests
import json
from pathlib import Path

def query_ollama(prompt: str, model: str = "codellama") -> None:
    """Send a streaming query to local Ollama instance."""
    print(f"Using {model} model for code analysis")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": True}
    )
    if not response.ok:
        raise RuntimeError(f"Query failed with status {response.status_code}")
    
    full_response = ""
    for line in response.iter_lines():
        if line:
            # Each line is a JSON object containing a piece of the response
            chunk = json.loads(line)
            if "response" in chunk:
                text_chunk = chunk["response"]
                full_response += text_chunk
                print(text_chunk, end="", flush=True)
            elif "error" in chunk:
                print(f"\nError from model: {chunk['error']}")
                return
    
    # Print a final newline
    if full_response:
        print("\n")

def get_directory_structure(directory: str = ".") -> str:
    """Get a string representation of the directory structure."""
    def _generate_tree(path: Path, prefix: str = "") -> str:
        tree = ""
        items = sorted(path.iterdir())
        for i, item in enumerate(items):
            if item.name.startswith('.') or item.name == '__pycache__':
                continue
            is_last = i == len(items) - 1
            tree += f"{prefix}{'└── ' if is_last else '├── '}{item.name}\n"
            if item.is_dir():
                tree += _generate_tree(item, prefix + ('    ' if is_last else '│   '))
        return tree
    return _generate_tree(Path(directory))

def get_directory_contents(directory: str = ".") -> dict[str, str]:
    """Get contents of all readable files in directory."""
    files_dict = {}
    file_count = 0
    skipped_count = 0
    
    for file_path in Path(directory).glob("*"):
        if file_path.is_file():
            if file_path.name.startswith('.') or file_path.name.endswith('.pyc'):
                skipped_count += 1
                continue
            try:
                files_dict[file_path.name] = file_path.read_text(encoding='utf-8')
                print(f"✓ Read {file_path.name}")
                file_count += 1
            except Exception as e:
                print(f"✗ Failed to read {file_path.name}: {e}")
                skipped_count += 1
    
    print(f"\nProcessed {file_count + skipped_count} total files:")
    print(f"- Successfully read: {file_count} files")
    print(f"- Skipped/failed: {skipped_count} files")
    return files_dict

def main() -> None:
    directory = "."
    print("Starting code analysis...")
    
    files = get_directory_contents(directory)
    directory_tree = get_directory_structure(directory)
    
    # Print a concise summary of the directory structure
    print("\nDirectory Structure Summary:")
    file_count = sum(1 for _ in Path(directory).rglob('*') if _.is_file())
    dir_count = sum(1 for _ in Path(directory).rglob('*') if _.is_dir())
    print(f"📁 {dir_count} directories, 📄 {file_count} files")
    
    files_description = "\n".join(
        f"File: {fname}\nContents:\n{contents}\n"
        for fname, contents in files.items()
    )
    
    prompt = f"""
Analyze this codebase directory. Keep responses factual and consistent. Focus on technical details rather than subjective assessment. Provide output in the following format:

OBJECTIVE
- Provide 2-3 clear sentences describing the overall purpose and functionality

KEY FILES
- List and describe up to 5 of the most important files, including:
  - File name
  - Purpose
  - Key outputs or functionality

ARCHITECTURE
- Describe the high-level architecture and key components in 2-3 bullet points

Please analyze these files:
{files_description}

For context, this is the directory structure:
{directory_tree}
    """.strip()
    
    try:
        print("\nAnalysis Result:\n----------------")
        query_ollama(prompt)
        print()  # Add newline after streaming completes
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
