from pathlib import Path
from typing import List, Dict, Any
import json
from tqdm import tqdm
from .agents.code_agent import CodeAgent
from .agents.doc_agent import DocAgent
from .agents.data_agent import DataAgent

class SwarmController:
    def __init__(self):
        """Initialize the swarm controller with all available agents"""
        self.agents = [
            CodeAgent(),
            DocAgent(),
            DataAgent()
        ]
        self.metadata_file = "metadata.json"
        self.load_metadata()
        
    def load_metadata(self):
        """Load existing metadata if available"""
        try:
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        except FileNotFoundError:
            self.metadata = {}
            
    def save_metadata(self):
        """Save metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
            
    def get_agent_for_file(self, file_path: Path):
        """Find the appropriate agent for a given file"""
        for agent in self.agents:
            if agent.can_handle_file(file_path):
                return agent
        return None
        
    def process_directory(self, directory: Path, recursive: bool = True) -> Dict[str, Any]:
        """Process all files in a directory"""
        results = {}
        
        # Get all files in directory
        pattern = "**/*" if recursive else "*"
        files = [f for f in Path(directory).glob(pattern) if f.is_file()]
        
        print(f"Processing {len(files)} files...")
        
        for file_path in tqdm(files):
            # Skip the metadata file itself
            if file_path.name == self.metadata_file:
                continue
                
            # Check if file has already been processed and hasn't changed
            file_stat = file_path.stat()
            file_key = str(file_path)
            
            if (file_key in self.metadata and 
                self.metadata[file_key].get("last_modified") == file_stat.st_mtime):
                results[file_key] = self.metadata[file_key]
                continue
                
            # Find appropriate agent
            agent = self.get_agent_for_file(file_path)
            if agent:
                # Process file
                analysis = agent.analyze_file(file_path)
                analysis["last_modified"] = file_stat.st_mtime
                analysis["agent"] = agent.name
                results[file_key] = analysis
            
        # Update metadata
        self.metadata.update(results)
        self.save_metadata()
        
        return results
        
    def get_tags_for_file(self, file_path: Path) -> List[str]:
        """Get tags for a specific file"""
        file_key = str(file_path)
        if file_key in self.metadata:
            return self.metadata[file_key].get("tags", [])
        return []
        
    def search_by_tag(self, tag: str) -> List[str]:
        """Find all files with a specific tag"""
        return [
            file_path
            for file_path, data in self.metadata.items()
            if tag.lower() in [t.lower() for t in data.get("tags", [])]
        ] 