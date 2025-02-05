import unittest
from pathlib import Path
from auto_tagger.agents.base_agent import BaseAgent

class TestAgent(BaseAgent):
    """Test implementation of BaseAgent for testing"""
    def __init__(self):
        super().__init__("TestAgent")
        self.supported_extensions = ['.test']
        
    def analyze_file(self, file_path: Path):
        return {"tags": ["test"], "metadata": {"test": True}}

class TestBaseAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TestAgent()
        
    def test_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.supported_extensions, ['.test'])
        
    def test_can_handle_file(self):
        """Test file type handling check"""
        test_file = Path("test.test")
        unsupported_file = Path("test.txt")
        
        self.assertTrue(self.agent.can_handle_file(test_file))
        self.assertFalse(self.agent.can_handle_file(unsupported_file))
        
    def test_get_file_content(self):
        """Test file content reading"""
        # Create a temporary test file
        test_content = "Test content"
        test_file = Path("test_file.txt")
        try:
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Test reading existing file
            content = self.agent.get_file_content(test_file)
            self.assertEqual(content, test_content)
            
            # Test reading non-existent file
            content = self.agent.get_file_content(Path("nonexistent.txt"))
            self.assertEqual(content, "")
            
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()

if __name__ == '__main__':
    unittest.main() 