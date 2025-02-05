#!/usr/bin/env python3
import os
from pathlib import Path
from auto_tagger import SwarmController
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Verify OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Initialize the swarm
    swarm = SwarmController()
    
    # Example: Process the current directory recursively
    print("\nProcessing current directory...")
    results = swarm.process_directory(Path("."), recursive=True)
    
    # Display results
    print(f"\nProcessed {len(results)} files")
    
    if results:
        print("\nSample of tagged files:")
        for file_path, data in list(results.items())[:5]:
            print(f"\nFile: {file_path}")
            print(f"Tags: {', '.join(data.get('tags', []))}")
            print(f"Agent: {data.get('agent', 'Unknown')}")
            if 'metadata' in data and 'analysis' in data['metadata']:
                print(f"Analysis: {data['metadata']['analysis']}")
    
    # Example: Search for files with specific tags
    example_tags = ['python', 'documentation', 'data']
    for tag in example_tags:
        files = swarm.search_by_tag(tag)
        if files:
            print(f"\nFiles tagged with '{tag}':")
            for file_path in files:
                print(f"  - {file_path}")

if __name__ == "__main__":
    main() 