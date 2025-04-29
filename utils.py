import hashlib
from typing import BinaryIO, List, Dict
import os
from pathlib import Path

def calculate_file_hash(file: BinaryIO) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    
    # Read the file in chunks to handle large files efficiently
    for chunk in iter(lambda: file.read(4096), b""):
        sha256_hash.update(chunk)
    
    # Reset file pointer to beginning for future reads
    file.seek(0)
    
    return sha256_hash.hexdigest()

def format_timestamp(timestamp: float) -> str:
    """Format timestamp into human-readable format."""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def process_directory(directory_path: str) -> List[Dict]:
    """Process all files in a directory and return their hashes."""
    results = []
    directory = Path(directory_path)
    
    if not directory.exists():
        raise ValueError(f"Directory {directory_path} does not exist")
    
    for file_path in directory.glob('**/*'):
        if file_path.is_file():
            try:
                with open(file_path, 'rb') as f:
                    file_hash = calculate_file_hash(f)
                    results.append({
                        'file_path': str(file_path),
                        'file_name': file_path.name,
                        'hash': file_hash
                    })
            except Exception as e:
                results.append({
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'error': str(e)
                })
    
    return results 