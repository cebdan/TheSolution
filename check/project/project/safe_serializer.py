#!/usr/bin/env python3
"""
Safe Serializer for TheSolution CAD
Replaces pickle with secure JSON serialization
"""

import json
import os
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import asdict, is_dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_SOLUTIONS = 10000
JSON_VERSION = "1.0"
FORMAT_NAME = "TheSolution_JSON"

class SolutionJSONEncoder:
    """Converts Solution objects to JSON-compatible dictionaries"""
    
    @staticmethod
    def solution_to_dict(solution) -> Dict[str, Any]:
        """Convert Solution object to dictionary"""
        try:
            if hasattr(solution, 'to_dict'):
                # Use object's own serialization method if available
                return solution.to_dict()
            
            # Handle dataclasses
            if is_dataclass(solution):
                return asdict(solution)
            
            # Handle SolutionCoordinate
            if hasattr(solution, 'x') and hasattr(solution, 'y') and hasattr(solution, 'z'):
                return {
                    'type': 'SolutionCoordinate',
                    'x': float(solution.x),
                    'y': float(solution.y),
                    'z': float(solution.z),
                    'a': float(getattr(solution, 'a', 0.0)),
                    'b': float(getattr(solution, 'b', 0.0)),
                    'c': float(getattr(solution, 'c', 0.0))
                }
            
            # Handle Solution objects
            if hasattr(solution, 'properties') and hasattr(solution, 'dimensions'):
                solution_type = getattr(solution.properties, 'solution_type', None)
                solution_type_value = solution_type.value if solution_type else 'UNKNOWN'
                
                data = {
                    'type': 'Solution',
                    'solution_type': solution_type_value,
                    'name': getattr(solution.properties, 'name', 'Unnamed'),
                    'coordinate': SolutionJSONEncoder.coordinate_to_dict(solution.properties.coordinate),
                    'dimensions': {},
                    'material': {},
                    'metadata': {}
                }
                
                # Handle SolutionIndex objects in properties
                if hasattr(solution.properties, 'index') and solution.properties.index is not None:
                    data['metadata']['index'] = str(solution.properties.index)
                
                # Add dimensions
                if hasattr(solution.dimensions, 'width'):
                    data['dimensions']['width'] = float(solution.dimensions.width)
                if hasattr(solution.dimensions, 'height'):
                    data['dimensions']['height'] = float(solution.dimensions.height)
                if hasattr(solution.dimensions, 'depth'):
                    data['dimensions']['depth'] = float(solution.dimensions.depth)
                if hasattr(solution.dimensions, 'radius'):
                    data['dimensions']['radius'] = float(solution.dimensions.radius)
                
                # Add material
                if hasattr(solution.properties, 'material') and solution.properties.material:
                    data['material'] = {
                        'name': getattr(solution.properties.material, 'name', 'Unknown'),
                        'density': float(getattr(solution.properties.material, 'density', 0.0))
                    }
                
                # Add metadata
                data['metadata'] = {
                    'created_at': getattr(solution, 'created_at', datetime.now().isoformat()),
                    'version': getattr(solution, 'version', '1.0'),
                    'id': str(getattr(solution, 'id', None)) if getattr(solution, 'id', None) is not None else None
                }
                
                # Handle parent/children relationships
                if hasattr(solution, 'parent') and solution.parent:
                    parent_id = getattr(solution.parent, 'id', None)
                    data['parent_id'] = str(parent_id) if parent_id is not None else None
                
                if hasattr(solution, 'children') and solution.children:
                    children_ids = [getattr(child, 'id', None) for child in solution.children]
                    data['children_ids'] = [str(child_id) if child_id is not None else None for child_id in children_ids]
                
                return data
            
            # Fallback for unknown objects
            logger.warning(f"Unknown object type: {type(solution)}")
            return {
                'type': 'Unknown',
                'class': solution.__class__.__name__,
                'data': str(solution)
            }
            
        except Exception as e:
            logger.error(f"Error serializing solution: {e}")
            return {
                'type': 'Error',
                'error': str(e),
                'class': solution.__class__.__name__ if hasattr(solution, '__class__') else 'Unknown'
            }
    
    @staticmethod
    def coordinate_to_dict(coordinate) -> Dict[str, Any]:
        """Convert SolutionCoordinate to dictionary"""
        if not coordinate:
            return {
                'type': 'SolutionCoordinate',
                'x': 0.0, 'y': 0.0, 'z': 0.0, 
                'a': 0.0, 'b': 0.0, 'c': 0.0
            }
        
        return {
            'type': 'SolutionCoordinate',
            'x': float(getattr(coordinate, 'x', 0.0)),
            'y': float(getattr(coordinate, 'y', 0.0)),
            'z': float(getattr(coordinate, 'z', 0.0)),
            'a': float(getattr(coordinate, 'a', 0.0)),
            'b': float(getattr(coordinate, 'b', 0.0)),
            'c': float(getattr(coordinate, 'c', 0.0))
        }
    
    @staticmethod
    def project_to_dict(solutions: List, metadata: Dict = None) -> Dict[str, Any]:
        """Create complete project structure"""
        if not metadata:
            metadata = {}
        
        # Convert solutions to dictionaries
        solutions_data = []
        for solution in solutions:
            try:
                solution_dict = SolutionJSONEncoder.solution_to_dict(solution)
                solutions_data.append(solution_dict)
            except Exception as e:
                logger.error(f"Error serializing solution: {e}")
                # Create a minimal representation
                solutions_data.append({
                    'type': 'Error',
                    'error': str(e),
                    'class': solution.__class__.__name__ if hasattr(solution, '__class__') else 'Unknown'
                })
        
        # Create project structure
        project_data = {
            'format': FORMAT_NAME,
            'version': JSON_VERSION,
            'created_at': datetime.now().isoformat(),
            'metadata': {
                'name': metadata.get('name', 'TheSolution Project'),
                'description': metadata.get('description', ''),
                'author': metadata.get('author', ''),
                'solutions_count': len(solutions_data),
                **metadata
            },
            'solutions': solutions_data
        }
        
        # Calculate checksum
        project_json = json.dumps(project_data, sort_keys=True, separators=(',', ':'))
        project_data['checksum'] = hashlib.sha256(project_json.encode()).hexdigest()
        
        return project_data

class SolutionJSONDecoder:
    """Converts JSON back to Solution objects"""
    
    @staticmethod
    def dict_to_solution(data: Dict[str, Any], parent=None):
        """Create Solution object from dictionary"""
        try:
            if data.get('type') == 'SolutionCoordinate':
                return SolutionJSONDecoder.dict_to_coordinate(data)
            
            if data.get('type') == 'Solution':
                return SolutionJSONDecoder.dict_to_solution_object(data, parent)
            
            logger.warning(f"Unknown solution type: {data.get('type')}")
            return None
            
        except Exception as e:
            logger.error(f"Error deserializing solution: {e}")
            return None
    
    @staticmethod
    def dict_to_coordinate(data: Dict[str, Any]):
        """Create SolutionCoordinate from dictionary"""
        try:
            from solution_data_types import SolutionCoordinate
            
            return SolutionCoordinate(
                x=data.get('x', 0.0),
                y=data.get('y', 0.0),
                z=data.get('z', 0.0),
                a=data.get('a', 0.0),
                b=data.get('b', 0.0),
                c=data.get('c', 0.0)
            )
        except ImportError:
            logger.error("solution_data_types not available")
            return None
    
    @staticmethod
    def dict_to_solution_object(data: Dict[str, Any], parent=None):
        """Create Solution object from dictionary"""
        try:
            from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
            
            # Create base solution
            solution_type_str = data.get('solution_type', 'BOX')
            try:
                solution_type = SolutionType(solution_type_str)
            except ValueError:
                # Handle case-insensitive mapping
                solution_type_str_upper = solution_type_str.upper()
                if solution_type_str_upper == 'BOX':
                    solution_type = SolutionType.BOX
                elif solution_type_str_upper == 'SPHERE':
                    solution_type = SolutionType.SPHERE
                elif solution_type_str_upper == 'CYLINDER':
                    solution_type = SolutionType.CYLINDER
                else:
                    solution_type = SolutionType.BOX  # Default fallback
            
            coordinate_data = data.get('coordinate', {})
            coordinate = SolutionCoordinate(
                x=coordinate_data.get('x', 0.0),
                y=coordinate_data.get('y', 0.0),
                z=coordinate_data.get('z', 0.0),
                a=coordinate_data.get('a', 0.0),
                b=coordinate_data.get('b', 0.0),
                c=coordinate_data.get('c', 0.0)
            )
            
            solution = SolutionDataUtils.create_minimal_solution_data(
                name=data.get('name', 'Unnamed'),
                solution_type=solution_type,
                coordinate=coordinate
            )
            
            # Set dimensions
            dimensions = data.get('dimensions', {})
            if 'width' in dimensions:
                solution.dimensions.width = float(dimensions['width'])
            if 'height' in dimensions:
                solution.dimensions.height = float(dimensions['height'])
            if 'depth' in dimensions:
                solution.dimensions.depth = float(dimensions['depth'])
            if 'radius' in dimensions:
                solution.dimensions.radius = float(dimensions['radius'])
            
            # Set material
            material_data = data.get('material', {})
            if material_data:
                solution.properties.material = SolutionMaterial(
                    name=material_data.get('name', 'Unknown'),
                    density=float(material_data.get('density', 0.0))
                )
            
            # Set metadata
            metadata = data.get('metadata', {})
            if 'created_at' in metadata:
                solution.created_at = metadata['created_at']
            if 'version' in metadata:
                solution.version = metadata['version']
            if 'id' in metadata and metadata['id'] is not None:
                solution.id = metadata['id']
            
            # Set parent
            if parent:
                solution.parent = parent
            
            return solution
            
        except ImportError:
            logger.error("solution_data_types not available")
            return None
        except Exception as e:
            logger.error(f"Error creating solution object: {e}")
            return None
    
    @staticmethod
    def dict_to_project(data: Dict[str, Any]) -> List:
        """Load complete project from dictionary"""
        try:
            # Validate format
            if data.get('format') != FORMAT_NAME:
                raise ValueError(f"Invalid format: {data.get('format')}")
            
            # Validate version
            if data.get('version') != JSON_VERSION:
                logger.warning(f"Version mismatch: expected {JSON_VERSION}, got {data.get('version')}")
            
            # Validate checksum
            if 'checksum' in data:
                project_copy = data.copy()
                stored_checksum = project_copy.pop('checksum')
                project_json = json.dumps(project_copy, sort_keys=True, separators=(',', ':'))
                calculated_checksum = hashlib.sha256(project_json.encode()).hexdigest()
                
                if stored_checksum != calculated_checksum:
                    raise ValueError("Checksum validation failed")
            
            # Convert solutions
            solutions = []
            solutions_data = data.get('solutions', [])
            
            for solution_data in solutions_data:
                solution = SolutionJSONDecoder.dict_to_solution(solution_data)
                if solution:
                    solutions.append(solution)
            
            return solutions
            
        except Exception as e:
            logger.error(f"Error loading project: {e}")
            return []

class SafeProjectManager:
    """Main API for saving/loading projects"""
    
    @staticmethod
    def save_project(solutions: List, filename: str, metadata: Dict = None) -> bool:
        """Save project to JSON file"""
        try:
            # Validate input
            if not solutions:
                logger.warning("No solutions to save")
                return False
            
            if len(solutions) > MAX_SOLUTIONS:
                raise ValueError(f"Too many solutions: {len(solutions)} > {MAX_SOLUTIONS}")
            
            # Create project data
            project_data = SolutionJSONEncoder.project_to_dict(solutions, metadata)
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Project saved successfully: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving project: {e}")
            return False
    
    @staticmethod
    def load_project(filename: str) -> List:
        """Load project from JSON file"""
        try:
            # Validate file
            if not SafeProjectManager.validate_project_file(filename):
                raise ValueError("Invalid project file")
            
            # Load JSON
            with open(filename, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            # Convert to solutions
            solutions = SolutionJSONDecoder.dict_to_project(project_data)
            
            logger.info(f"Project loaded successfully: {filename} ({len(solutions)} solutions)")
            return solutions
            
        except Exception as e:
            logger.error(f"Error loading project: {e}")
            return []
    
    @staticmethod
    def validate_project_file(filename: str) -> bool:
        """Validate project file without loading"""
        try:
            # Check file exists
            if not os.path.exists(filename):
                return False
            
            # Check file size
            file_size = os.path.getsize(filename)
            if file_size > MAX_FILE_SIZE:
                logger.error(f"File too large: {file_size} > {MAX_FILE_SIZE}")
                return False
            
            # Check file extension
            if not filename.lower().endswith(('.json', '.3d_sol')):
                logger.warning(f"Unexpected file extension: {filename}")
            
            # Try to parse JSON header
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    # Read first few lines to check format
                    header = f.read(1024)
                    if FORMAT_NAME not in header:
                        logger.error(f"Invalid format in file: {filename}")
                        return False
            except Exception as e:
                logger.error(f"Error reading file {filename}: {e}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating file {filename}: {e}")
            return False
    
    @staticmethod
    def get_project_info(filename: str) -> Dict[str, Any]:
        """Get project information without loading all data"""
        try:
            if not SafeProjectManager.validate_project_file(filename):
                return {}
            
            with open(filename, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            return {
                'format': project_data.get('format'),
                'version': project_data.get('version'),
                'created_at': project_data.get('created_at'),
                'metadata': project_data.get('metadata', {}),
                'solutions_count': len(project_data.get('solutions', [])),
                'file_size': os.path.getsize(filename)
            }
            
        except Exception as e:
            logger.error(f"Error getting project info: {e}")
            return {}
