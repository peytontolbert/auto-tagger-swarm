import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import tempfile
import shutil
from auto_tagger.swarm_controller import SwarmController

class TestSwarmController(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for test files
        self.test_dir = Path(tempfile.mkdtemp())
        self.swarm = SwarmController()
        
        # Create test files
        self.create_test_files()
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
        if Path("metadata.json").exists():
            Path("metadata.json").unlink()
            
    def create_test_files(self):
        """Create test files of different types"""
        # Python file
        with open(self.test_dir / "test.py", 'w') as f:
            f.write("def test(): pass")
            
        # Markdown file
        with open(self.test_dir / "test.md", 'w') as f:
            f.write("# Test\nThis is a test")
            
        # JSON file
        with open(self.test_dir / "test.json", 'w') as f:
            json.dump({"test": "data"}, f)
            
    def test_initialization(self):
        """Test SwarmController initialization"""
        self.assertEqual(len(self.swarm.agents), 3)  # Should have 3 specialized agents
        self.assertEqual(self.swarm.metadata_file, "metadata.json")
        
    def test_get_agent_for_file(self):
        """Test agent selection for different file types"""
        # Test Python file
        agent = self.swarm.get_agent_for_file(Path("test.py"))
        self.assertEqual(agent.name, "CodeAgent")
        
        # Test Markdown file
        agent = self.swarm.get_agent_for_file(Path("test.md"))
        self.assertEqual(agent.name, "DocAgent")
        
        # Test JSON file
        agent = self.swarm.get_agent_for_file(Path("test.json"))
        self.assertEqual(agent.name, "DataAgent")
        
        # Test unsupported file
        agent = self.swarm.get_agent_for_file(Path("test.unknown"))
        self.assertIsNone(agent)
        
    @patch('auto_tagger.agents.code_agent.CodeAgent.analyze_file')
    @patch('auto_tagger.agents.doc_agent.DocAgent.analyze_file')
    @patch('auto_tagger.agents.data_agent.DataAgent.analyze_file')
    def test_process_directory(self, mock_data_agent, mock_doc_agent, mock_code_agent):
        """Test directory processing"""
        # Mock agent responses
        mock_code_agent.return_value = {"tags": ["python"], "metadata": {"test": True}}
        mock_doc_agent.return_value = {"tags": ["documentation"], "metadata": {"test": True}}
        mock_data_agent.return_value = {"tags": ["data"], "metadata": {"test": True}}
        
        # Process directory
        results = self.swarm.process_directory(self.test_dir)
        
        # Verify results
        self.assertEqual(len(results), 3)  # Should process 3 test files
        self.assertTrue(any(str(self.test_dir / "test.py") in key for key in results))
        self.assertTrue(any(str(self.test_dir / "test.md") in key for key in results))
        self.assertTrue(any(str(self.test_dir / "test.json") in key for key in results))
        
    def test_metadata_persistence(self):
        """Test metadata saving and loading"""
        test_metadata = {
            "test.py": {
                "tags": ["python"],
                "metadata": {"test": True},
                "last_modified": 123456789
            }
        }
        
        # Save metadata
        self.swarm.metadata = test_metadata
        self.swarm.save_metadata()
        
        # Create new controller to test loading
        new_swarm = SwarmController()
        self.assertEqual(new_swarm.metadata, test_metadata)
        
    def test_search_by_tag(self):
        """Test tag search functionality"""
        # Add test metadata
        self.swarm.metadata = {
            "test1.py": {"tags": ["python", "web"]},
            "test2.py": {"tags": ["python", "cli"]},
            "test3.js": {"tags": ["javascript", "web"]}
        }
        
        # Search for tags
        python_files = self.swarm.search_by_tag("python")
        web_files = self.swarm.search_by_tag("web")
        
        self.assertEqual(len(python_files), 2)
        self.assertEqual(len(web_files), 2)
        self.assertIn("test1.py", python_files)
        self.assertIn("test2.py", python_files)
        self.assertIn("test1.py", web_files)
        self.assertIn("test3.js", web_files)

if __name__ == '__main__':
    unittest.main() 