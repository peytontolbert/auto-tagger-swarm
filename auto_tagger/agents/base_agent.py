from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from pathlib import Path

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.supported_extensions: List[str] = []
    
    @abstractmethod
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a file and return tags and metadata
        Args:
            file_path: Path to the file to analyze
        Returns:
            Dictionary containing tags and metadata
        """
        pass
    
    def can_handle_file(self, file_path: Path) -> bool:
        """Check if this agent can handle the given file type"""
        return file_path.suffix.lower() in self.supported_extensions
    
    def get_file_content(self, file_path: Path) -> str:
        """Read and return file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return "" 