import argparse
from pathlib import Path
from .swarm_controller import SwarmController

def main():
    parser = argparse.ArgumentParser(description='Auto-tag files using a swarm of specialized agents')
    parser.add_argument('directory', type=str, help='Directory to process')
    parser.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
    parser.add_argument('--search', '-s', type=str, help='Search for files with a specific tag')
    
    args = parser.parse_args()
    
    swarm = SwarmController()
    
    if args.search:
        # Search mode
        results = swarm.search_by_tag(args.search)
        if results:
            print(f"\nFiles tagged with '{args.search}':")
            for file_path in results:
                print(f"  - {file_path}")
        else:
            print(f"\nNo files found with tag '{args.search}'")
    else:
        # Processing mode
        directory = Path(args.directory)
        if not directory.exists():
            print(f"Error: Directory '{directory}' does not exist")
            return
            
        print(f"\nProcessing directory: {directory}")
        results = swarm.process_directory(directory, args.recursive)
        
        print("\nProcessing complete!")
        print(f"Processed {len(results)} files")
        
        # Show sample of results
        print("\nSample of tagged files:")
        for file_path, data in list(results.items())[:5]:
            print(f"\n{file_path}:")
            print(f"  Tags: {', '.join(data.get('tags', []))}")
            print(f"  Agent: {data.get('agent', 'Unknown')}")

if __name__ == "__main__":
    main() 