from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv
from openai import OpenAI
from .base_agent import BaseAgent

load_dotenv()

class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeAgent")
        self.supported_extensions = ['.py', '.js', '.java', '.cpp', '.ts', '.go', '.rs']
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a code file and generate relevant tags"""
        content = self.get_file_content(file_path)
        if not content:
            return {"tags": [], "metadata": {"error": "Empty file or error reading file"}}
            
        # Create a prompt for the language model
        prompt = f"""Analyze this code file and provide:
        1. Programming language
        2. Main functionality/purpose
        3. Key components/classes
        4. Important dependencies
        5. Relevant tags (max 5)
        
        Code:
        {content[:1500]}  # Limit content length for API
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a code analysis expert. Provide concise, relevant tags and metadata for code files."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            analysis = response.choices[0].message.content
            
            # Parse the response into structured data
            # This is a simple implementation - you might want to make it more robust
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