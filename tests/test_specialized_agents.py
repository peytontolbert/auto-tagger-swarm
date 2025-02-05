import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
from auto_tagger.agents.code_agent import CodeAgent
from auto_tagger.agents.doc_agent import DocAgent
from auto_tagger.agents.data_agent import DataAgent

class TestCodeAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CodeAgent()
        
    def test_initialization(self):
        """Test CodeAgent initialization"""
        self.assertEqual(self.agent.name, "CodeAgent")
        self.assertIn('.py', self.agent.supported_extensions)
        self.assertIn('.js', self.agent.supported_extensions)
        
    @patch('openai.OpenAI')
    def test_analyze_file(self, mock_openai):
        """Test code file analysis"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Python code file\nWeb server\nFlask application"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Create test file
        test_file = Path("test.py")
        test_content = "def hello(): print('Hello, World!')"
        
        try:
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            result = self.agent.analyze_file(test_file)
            
            self.assertIn('tags', result)
            self.assertIn('metadata', result)
            self.assertEqual(result['metadata']['file_type'], '.py')
            
        finally:
            if test_file.exists():
                test_file.unlink()

class TestDocAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DocAgent()
        
    def test_initialization(self):
        """Test DocAgent initialization"""
        self.assertEqual(self.agent.name, "DocAgent")
        self.assertIn('.md', self.agent.supported_extensions)
        self.assertIn('.txt', self.agent.supported_extensions)
        
    @patch('openai.OpenAI')
    def test_analyze_file(self, mock_openai):
        """Test documentation file analysis"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Markdown documentation\nProject setup\nInstallation guide"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Create test file
        test_file = Path("test.md")
        test_content = "# Test Documentation\n\nThis is a test."
        
        try:
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            result = self.agent.analyze_file(test_file)
            
            self.assertIn('tags', result)
            self.assertIn('metadata', result)
            self.assertEqual(result['metadata']['file_type'], '.md')
            
        finally:
            if test_file.exists():
                test_file.unlink()

class TestDataAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DataAgent()
        
    def test_initialization(self):
        """Test DataAgent initialization"""
        self.assertEqual(self.agent.name, "DataAgent")
        self.assertIn('.json', self.agent.supported_extensions)
        self.assertIn('.csv', self.agent.supported_extensions)
        
    @patch('openai.OpenAI')
    def test_analyze_json_file(self, mock_openai):
        """Test JSON file analysis"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="JSON data\nConfiguration file\nSettings"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Create test file
        test_file = Path("test.json")
        test_content = json.dumps({"test": "data", "key": "value"})
        
        try:
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            result = self.agent.analyze_file(test_file)
            
            self.assertIn('tags', result)
            self.assertIn('metadata', result)
            self.assertEqual(result['metadata']['file_type'], '.json')
            
        finally:
            if test_file.exists():
                test_file.unlink()

if __name__ == '__main__':
    unittest.main() 