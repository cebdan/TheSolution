#!/usr/bin/env python3
"""
Tests for safe JSON serialization
"""

import pytest
import json
import os
import tempfile
import shutil
from datetime import datetime

# Add project path
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from project.safe_serializer import (
    SolutionJSONEncoder, 
    SolutionJSONDecoder, 
    SafeProjectManager,
    MAX_FILE_SIZE,
    MAX_SOLUTIONS
)

# Import solution types
try:
    from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
    SOLUTION_TYPES_AVAILABLE = True
except ImportError:
    SOLUTION_TYPES_AVAILABLE = False

@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_solution():
    """Create sample solution for testing"""
    if not SOLUTION_TYPES_AVAILABLE:
        pytest.skip("Solution types not available")
    
    solution = SolutionDataUtils.create_minimal_solution_data(
        name="Test Box",
        solution_type=SolutionType.BOX,
        coordinate=SolutionCoordinate(10, 20, 30)
    )
    solution.dimensions.width = 100.0
    solution.dimensions.height = 50.0
    solution.dimensions.depth = 25.0
    solution.properties.material = SolutionMaterial(name="Steel", density=7.85)
    solution.created_at = datetime.now().isoformat()
    solution.version = "1.0"
    solution.id = "test_001"
    
    return solution

@pytest.fixture
def sample_coordinate():
    """Create sample coordinate for testing"""
    if not SOLUTION_TYPES_AVAILABLE:
        pytest.skip("Solution types not available")
    
    return SolutionCoordinate(1.5, 2.5, 3.5, 0.1, 0.2, 0.3)

class TestSolutionJSONEncoder:
    """Test SolutionJSONEncoder class"""
    
    def test_coordinate_to_dict(self, sample_coordinate):
        """Test coordinate serialization"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        coord_dict = SolutionJSONEncoder.coordinate_to_dict(sample_coordinate)
        
        assert coord_dict['x'] == 1.5
        assert coord_dict['y'] == 2.5
        assert coord_dict['z'] == 3.5
        assert coord_dict['a'] == 0.1
        assert coord_dict['b'] == 0.2
        assert coord_dict['c'] == 0.3
        assert coord_dict['type'] == 'SolutionCoordinate'
    
    def test_solution_to_dict(self, sample_solution):
        """Test solution serialization"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        solution_dict = SolutionJSONEncoder.solution_to_dict(sample_solution)
        
        assert solution_dict['type'] == 'Solution'
        assert solution_dict['solution_type'] == 'BOX'
        assert solution_dict['name'] == 'Test Box'
        assert solution_dict['dimensions']['width'] == 100.0
        assert solution_dict['dimensions']['height'] == 50.0
        assert solution_dict['dimensions']['depth'] == 25.0
        assert solution_dict['material']['name'] == 'Steel'
        assert solution_dict['material']['density'] == 7.85
        assert solution_dict['metadata']['id'] == 'test_001'
    
    def test_project_to_dict(self, sample_solution):
        """Test project serialization"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        solutions = [sample_solution]
        metadata = {'name': 'Test Project', 'description': 'Test description'}
        
        project_dict = SolutionJSONEncoder.project_to_dict(solutions, metadata)
        
        assert project_dict['format'] == 'TheSolution_JSON'
        assert project_dict['version'] == '1.0'
        assert project_dict['metadata']['name'] == 'Test Project'
        assert project_dict['metadata']['description'] == 'Test description'
        assert project_dict['metadata']['solutions_count'] == 1
        assert len(project_dict['solutions']) == 1
        assert 'checksum' in project_dict

class TestSolutionJSONDecoder:
    """Test SolutionJSONDecoder class"""
    
    def test_dict_to_coordinate(self):
        """Test coordinate deserialization"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        coord_dict = {
            'type': 'SolutionCoordinate',
            'x': 1.5, 'y': 2.5, 'z': 3.5,
            'a': 0.1, 'b': 0.2, 'c': 0.3
        }
        
        coordinate = SolutionJSONDecoder.dict_to_coordinate(coord_dict)
        
        assert coordinate.x == 1.5
        assert coordinate.y == 2.5
        assert coordinate.z == 3.5
        assert coordinate.a == 0.1
        assert coordinate.b == 0.2
        assert coordinate.c == 0.3
    
    def test_dict_to_solution(self, sample_solution):
        """Test solution deserialization"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        # First serialize
        solution_dict = SolutionJSONEncoder.solution_to_dict(sample_solution)
        
        # Then deserialize
        restored_solution = SolutionJSONDecoder.dict_to_solution(solution_dict)
        
        assert restored_solution is not None
        assert restored_solution.properties.name == 'Test Box'
        assert restored_solution.properties.solution_type == SolutionType.BOX
        assert restored_solution.dimensions.width == 100.0
        assert restored_solution.dimensions.height == 50.0
        assert restored_solution.dimensions.depth == 25.0
        assert restored_solution.properties.material.name == 'Steel'
        assert restored_solution.properties.material.density == 7.85
    
    def test_dict_to_project(self, sample_solution):
        """Test project deserialization"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        # Create project data
        solutions = [sample_solution]
        project_dict = SolutionJSONEncoder.project_to_dict(solutions)
        
        # Deserialize
        restored_solutions = SolutionJSONDecoder.dict_to_project(project_dict)
        
        assert len(restored_solutions) == 1
        assert restored_solutions[0].properties.name == 'Test Box'

class TestSafeProjectManager:
    """Test SafeProjectManager class"""
    
    def test_save_and_load_project(self, sample_solution, temp_dir):
        """Test save and load functionality"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        filename = os.path.join(temp_dir, "test_project.json")
        solutions = [sample_solution]
        metadata = {'name': 'Test Project'}
        
        # Save project
        success = SafeProjectManager.save_project(solutions, filename, metadata)
        assert success is True
        assert os.path.exists(filename)
        
        # Load project
        loaded_solutions = SafeProjectManager.load_project(filename)
        assert len(loaded_solutions) == 1
        assert loaded_solutions[0].properties.name == 'Test Box'
    
    def test_validate_project_file(self, sample_solution, temp_dir):
        """Test file validation"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        filename = os.path.join(temp_dir, "test_project.json")
        solutions = [sample_solution]
        
        # Save valid project
        SafeProjectManager.save_project(solutions, filename)
        assert SafeProjectManager.validate_project_file(filename) is True
        
        # Test non-existent file
        assert SafeProjectManager.validate_project_file("nonexistent.json") is False
    
    def test_get_project_info(self, sample_solution, temp_dir):
        """Test project info retrieval"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        filename = os.path.join(temp_dir, "test_project.json")
        solutions = [sample_solution]
        metadata = {'name': 'Test Project', 'author': 'Test Author'}
        
        SafeProjectManager.save_project(solutions, filename, metadata)
        info = SafeProjectManager.get_project_info(filename)
        
        assert info['format'] == 'TheSolution_JSON'
        assert info['version'] == '1.0'
        assert info['metadata']['name'] == 'Test Project'
        assert info['metadata']['author'] == 'Test Author'
        assert info['solutions_count'] == 1
        assert 'file_size' in info

class TestSecurity:
    """Test security features"""
    
    def test_large_file_protection(self, temp_dir):
        """Test protection against large files"""
        # Create a large file
        large_file = os.path.join(temp_dir, "large_file.json")
        
        # Create a large JSON structure
        large_data = {
            'format': 'TheSolution_JSON',
            'version': '1.0',
            'solutions': [{'type': 'Solution', 'data': 'x' * 1000}] * 100000
        }
        
        with open(large_file, 'w') as f:
            json.dump(large_data, f)
        
        # Should fail validation due to size
        assert SafeProjectManager.validate_project_file(large_file) is False
    
    def test_malicious_json(self, temp_dir):
        """Test protection against malicious JSON"""
        malicious_file = os.path.join(temp_dir, "malicious.json")
        
        # Create JSON with suspicious content
        malicious_data = {
            'format': 'TheSolution_JSON',
            'version': '1.0',
            'solutions': [
                {
                    'type': 'Solution',
                    'solution_type': 'BOX',
                    'name': 'Malicious',
                    'coordinate': {'x': 0, 'y': 0, 'z': 0},
                    'dimensions': {'width': 10, 'height': 10, 'depth': 10},
                    'metadata': {
                        'created_at': '2023-01-01T00:00:00',
                        'version': '1.0',
                        'id': 'malicious_001'
                    }
                }
            ]
        }
        
        with open(malicious_file, 'w') as f:
            json.dump(malicious_data, f)
        
        # Should pass validation (no code execution)
        assert SafeProjectManager.validate_project_file(malicious_file) is True
        
        # Should load without executing code
        solutions = SafeProjectManager.load_project(malicious_file)
        assert len(solutions) == 1
        assert solutions[0].properties.name == 'Malicious'
    
    def test_invalid_format(self, temp_dir):
        """Test rejection of invalid format"""
        invalid_file = os.path.join(temp_dir, "invalid.json")
        
        invalid_data = {
            'format': 'InvalidFormat',
            'version': '1.0',
            'solutions': []
        }
        
        with open(invalid_file, 'w') as f:
            json.dump(invalid_data, f)
        
        # Should fail validation
        assert SafeProjectManager.validate_project_file(invalid_file) is False

class TestCompatibility:
    """Test compatibility features"""
    
    def test_empty_solutions(self, temp_dir):
        """Test handling of empty solutions list"""
        filename = os.path.join(temp_dir, "empty_project.json")
        
        # Should handle empty list gracefully
        success = SafeProjectManager.save_project([], filename)
        assert success is False  # No solutions to save
        
        # But should create file with empty structure
        if os.path.exists(filename):
            loaded_solutions = SafeProjectManager.load_project(filename)
            assert len(loaded_solutions) == 0
    
    def test_multiple_solution_types(self, temp_dir):
        """Test multiple solution types"""
        if not SOLUTION_TYPES_AVAILABLE:
            pytest.skip("Solution types not available")
        
        # Create different solution types
        box_solution = SolutionDataUtils.create_minimal_solution_data(
            name="Test Box",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        box_solution.dimensions.width = 10
        box_solution.dimensions.height = 10
        box_solution.dimensions.depth = 10
        
        sphere_solution = SolutionDataUtils.create_minimal_solution_data(
            name="Test Sphere",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(20, 0, 0)
        )
        sphere_solution.dimensions.radius = 5
        
        solutions = [box_solution, sphere_solution]
        filename = os.path.join(temp_dir, "multi_types.json")
        
        # Save and load
        SafeProjectManager.save_project(solutions, filename)
        loaded_solutions = SafeProjectManager.load_project(filename)
        
        assert len(loaded_solutions) == 2
        assert loaded_solutions[0].properties.solution_type == SolutionType.BOX
        assert loaded_solutions[1].properties.solution_type == SolutionType.SPHERE

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
