"""
Auto-Tagger Swarm
================

A lightweight swarm of specialized agents that automatically tag files based on their contents
using natural language processing (NLP).

Each agent specializes in analyzing specific file types:
- CodeAgent: Analyzes programming code files
- DocAgent: Analyzes documentation and text files
- DataAgent: Analyzes data files (JSON, CSV, etc.)

Usage:
    from auto_tagger.swarm_controller import SwarmController
    
    # Create swarm controller
    swarm = SwarmController()
    
    # Process a directory
    results = swarm.process_directory("path/to/directory")
    
    # Search for files with a specific tag
    files = swarm.search_by_tag("python")
"""

from .swarm_controller import SwarmController
from .agents.base_agent import BaseAgent
from .agents.code_agent import CodeAgent
from .agents.doc_agent import DocAgent
from .agents.data_agent import DataAgent

__version__ = "0.1.0"
__all__ = ['SwarmController', 'BaseAgent', 'CodeAgent', 'DocAgent', 'DataAgent'] 