#!/usr/bin/env python3
"""
Migration utility for converting pickle files to JSON
"""

import os
import sys
import json
import pickle
import shutil
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add project path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from project.safe_serializer import SafeProjectManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PickleToJSONMigrator:
    """Migrate pickle files to JSON format"""
    
    def __init__(self, backup_dir: str = None):
        self.backup_dir = backup_dir or "pickle_backups"
        self.migration_log = []
        
    def find_pickle_files(self, directory: str) -> List[str]:
        """Find all pickle files in directory"""
        pickle_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.pickle', '.pkl')):
                    pickle_files.append(os.path.join(root, file))
        
        return pickle_files
    
    def backup_file(self, filepath: str) -> str:
        """Create backup of original file"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{timestamp}_{filename}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        shutil.copy2(filepath, backup_path)
        logger.info(f"Backup created: {backup_path}")
        
        return backup_path
    
    def load_pickle_data(self, filepath: str) -> Any:
        """Safely load pickle data"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            return data
        except Exception as e:
            logger.error(f"Error loading pickle file {filepath}: {e}")
            return None
    
    def convert_pickle_to_json(self, filepath: str) -> bool:
        """Convert single pickle file to JSON"""
        try:
            logger.info(f"Converting: {filepath}")
            
            # Load pickle data
            pickle_data = self.load_pickle_data(filepath)
            if pickle_data is None:
                return False
            
            # Create backup
            backup_path = self.backup_file(filepath)
            
            # Convert to JSON
            json_filepath = filepath.rsplit('.', 1)[0] + '.json'
            
            # Handle different data types
            if isinstance(pickle_data, list):
                # Assume it's a list of solutions
                success = SafeProjectManager.save_project(
                    pickle_data, 
                    json_filepath,
                    metadata={'migrated_from': filepath, 'migration_date': datetime.now().isoformat()}
                )
            elif isinstance(pickle_data, dict):
                # Assume it's a project structure
                if 'solutions' in pickle_data:
                    solutions = pickle_data['solutions']
                    metadata = pickle_data.get('metadata', {})
                    metadata['migrated_from'] = filepath
                    metadata['migration_date'] = datetime.now().isoformat()
                    
                    success = SafeProjectManager.save_project(solutions, json_filepath, metadata)
                else:
                    # Save as plain JSON
                    with open(json_filepath, 'w', encoding='utf-8') as f:
                        json.dump(pickle_data, f, indent=2, ensure_ascii=False)
                    success = True
            else:
                # Save as plain JSON
                with open(json_filepath, 'w', encoding='utf-8') as f:
                    json.dump(pickle_data, f, indent=2, ensure_ascii=False)
                success = True
            
            if success:
                logger.info(f"Successfully converted: {filepath} -> {json_filepath}")
                self.migration_log.append({
                    'original': filepath,
                    'json': json_filepath,
                    'backup': backup_path,
                    'status': 'success',
                    'timestamp': datetime.now().isoformat()
                })
                return True
            else:
                logger.error(f"Failed to convert: {filepath}")
                self.migration_log.append({
                    'original': filepath,
                    'status': 'failed',
                    'timestamp': datetime.now().isoformat()
                })
                return False
                
        except Exception as e:
            logger.error(f"Error converting {filepath}: {e}")
            self.migration_log.append({
                'original': filepath,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def migrate_directory(self, directory: str) -> Dict[str, Any]:
        """Migrate all pickle files in directory"""
        logger.info(f"Starting migration of directory: {directory}")
        
        pickle_files = self.find_pickle_files(directory)
        logger.info(f"Found {len(pickle_files)} pickle files")
        
        results = {
            'total_files': len(pickle_files),
            'successful': 0,
            'failed': 0,
            'errors': 0,
            'files': []
        }
        
        for filepath in pickle_files:
            try:
                success = self.convert_pickle_to_json(filepath)
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                logger.error(f"Unexpected error processing {filepath}: {e}")
                results['errors'] += 1
        
        results['files'] = self.migration_log
        
        logger.info(f"Migration completed: {results['successful']} successful, "
                   f"{results['failed']} failed, {results['errors']} errors")
        
        return results
    
    def validate_migration(self, original_file: str, json_file: str) -> bool:
        """Validate that migration was successful"""
        try:
            # Load original pickle
            pickle_data = self.load_pickle_data(original_file)
            if pickle_data is None:
                return False
            
            # Load JSON
            if not SafeProjectManager.validate_project_file(json_file):
                return False
            
            json_solutions = SafeProjectManager.load_project(json_file)
            
            # Basic validation
            if isinstance(pickle_data, list):
                if len(pickle_data) != len(json_solutions):
                    logger.warning(f"Solution count mismatch: {len(pickle_data)} vs {len(json_solutions)}")
                    return False
            elif isinstance(pickle_data, dict) and 'solutions' in pickle_data:
                if len(pickle_data['solutions']) != len(json_solutions):
                    logger.warning(f"Solution count mismatch: {len(pickle_data['solutions'])} vs {len(json_solutions)}")
                    return False
            
            logger.info(f"Migration validation successful: {original_file}")
            return True
            
        except Exception as e:
            logger.error(f"Migration validation failed: {e}")
            return False
    
    def save_migration_report(self, results: Dict[str, Any], output_file: str = None):
        """Save migration report"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"migration_report_{timestamp}.json"
        
        report = {
            'migration_date': datetime.now().isoformat(),
            'summary': {
                'total_files': results['total_files'],
                'successful': results['successful'],
                'failed': results['failed'],
                'errors': results['errors'],
                'success_rate': results['successful'] / results['total_files'] if results['total_files'] > 0 else 0
            },
            'files': results['files']
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Migration report saved: {output_file}")
        return output_file

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Migrate pickle files to JSON format')
    parser.add_argument('directory', help='Directory to search for pickle files')
    parser.add_argument('--backup-dir', default='pickle_backups', help='Backup directory')
    parser.add_argument('--validate', action='store_true', help='Validate migrations')
    parser.add_argument('--report', help='Output file for migration report')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no actual conversion)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        logger.error(f"Directory does not exist: {args.directory}")
        return 1
    
    migrator = PickleToJSONMigrator(args.backup_dir)
    
    if args.test:
        logger.info("Running in test mode")
        pickle_files = migrator.find_pickle_files(args.directory)
        logger.info(f"Found {len(pickle_files)} pickle files:")
        for filepath in pickle_files:
            logger.info(f"  - {filepath}")
        return 0
    
    # Perform migration
    results = migrator.migrate_directory(args.directory)
    
    # Validate if requested
    if args.validate:
        logger.info("Validating migrations...")
        for file_info in results['files']:
            if file_info['status'] == 'success':
                original = file_info['original']
                json_file = file_info['json']
                if not migrator.validate_migration(original, json_file):
                    logger.warning(f"Validation failed for: {original}")
    
    # Save report
    report_file = migrator.save_migration_report(results, args.report)
    
    # Print summary
    print(f"\nMigration Summary:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Errors: {results['errors']}")
    print(f"  Success rate: {results['successful']/results['total_files']*100:.1f}%" if results['total_files'] > 0 else "  Success rate: 0%")
    print(f"  Report saved: {report_file}")
    
    return 0 if results['failed'] == 0 and results['errors'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
