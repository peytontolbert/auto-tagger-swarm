# Auto-Tagger Swarm

A lightweight swarm of specialized agents that automatically tag files based on their contents using natural language processing (NLP). Each agent specializes in analyzing specific file types, making the tagging process more accurate and context-aware.

## Features

- **Specialized Agents**:
  - CodeAgent: Analyzes programming code files (.py, .js, .java, etc.)
  - DocAgent: Analyzes documentation and text files (.md, .txt, .rst, etc.)
  - DataAgent: Analyzes data files (.json, .csv, .xlsx, etc.)

- **Smart Tagging**: Uses OpenAI's GPT models to generate relevant tags based on file content
- **Efficient Processing**: Only processes files that have changed since last run
- **Metadata Storage**: Saves all tags and metadata for quick lookup
- **Command Line Interface**: Easy to use CLI for processing directories and searching tags

## Installation

1. Clone the repository:
```bash
git clone https://github.com/peytontolbert/auto-tagger-swarm.git
cd auto-tagger-swarm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

1. Process a directory:
```bash
python -m auto_tagger /path/to/directory
```

2. Process a directory recursively:
```bash
python -m auto_tagger /path/to/directory -r
```

3. Search for files with a specific tag:
```bash
python -m auto_tagger /path/to/directory -s python
```

### Python API

```python
from auto_tagger import SwarmController

# Create swarm controller
swarm = SwarmController()

# Process a directory
results = swarm.process_directory("path/to/directory", recursive=True)

# Search for files with a specific tag
files = swarm.search_by_tag("python")

# Get tags for a specific file
tags = swarm.get_tags_for_file("path/to/file.py")
```

## How It Works

1. The swarm controller identifies the appropriate agent for each file based on its extension
2. The specialized agent reads and analyzes the file content
3. The agent uses GPT to generate relevant tags and metadata
4. Results are stored in a metadata.json file for future reference
5. Only changed files are reprocessed in subsequent runs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 