from pathlib import Path
from typing import Dict, Any
import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from .base_agent import BaseAgent

load_dotenv()

class DataAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataAgent")
        self.supported_extensions = ['.json', '.csv', '.xlsx', '.xml', '.yaml', '.yml']
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a data file and generate relevant tags"""
        try:
            # Handle different file types
            if file_path.suffix == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                sample = str(dict(list(data.items())[:5])) if isinstance(data, dict) else str(data[:5])
            elif file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
                sample = f"Columns: {', '.join(df.columns[:10])}\nSample data:\n{df.head(3).to_string()}"
            else:
                content = self.get_file_content(file_path)
                sample = content[:1500]
                
            # Create a prompt for the language model
            prompt = f"""Analyze this data file and provide:
            1. Data format/structure
            2. Key data fields/columns
            3. Data purpose/content type
            4. Data characteristics
            5. Relevant tags (max 5)
            
            Sample data:
            {sample}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data analysis expert. Provide concise, relevant tags and metadata for data files."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            analysis = response.choices[0].message.content
            
            # Extract tags from the analysis
            tags = [word.strip() for word in analysis.lower().split() if len(word) > 3][:5]
            
            return {
                "tags": tags,
                "metadata": {
                    "file_type": file_path.suffix,
                    "analysis": analysis,
                    "size": os.path.getsize(file_path)
                }
            }
            
        except Exception as e:
            return {
                "tags": [],
                "metadata": {
                    "error": str(e)
                }
            } 