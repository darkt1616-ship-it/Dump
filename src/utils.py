"""
Utility functions for breach research toolkit
"""

import os
import sys
import time
import logging
import psutil
import hashlib
from pathlib import Path
from functools import wraps
from typing import Optional, Union, Dict, Any
import json
import yaml

def setup_logging(
    name: str = "breach_research",
    log_file: Optional[str] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        name: Logger name
        log_file: Optional log file path
        level: Logging level
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Crea formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (opzionale)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_memory_usage() -> Dict[str, Any]:
    """
    Get current memory usage
    
    Returns:
        Dict with memory information
    """
    mem = psutil.virtual_memory()
    process = psutil.Process(os.getpid())
    
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent,
        "process_used": process.memory_info().rss,
        "process_percent": process.memory_percent(),
    }

def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human readable string
    
    Args:
        bytes_value: Bytes to format
    
    Returns:
        Formatted string (e.g., "1.23 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def timer(func):
    """
    Decorator to measure function execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"⏱️ {func.__name__} eseguito in {elapsed:.2f} secondi")
        return result
    return wrapper

def validate_file(file_path: Union[str, Path]) -> bool:
    """
    Validate if file exists and is readable
    
    Args:
        file_path: Path to file
    
    Returns:
        True if valid, False otherwise
    """
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File non trovato: {file_path}")
        return False
    
    if not path.is_file():
        print(f"❌ Non è un file: {file_path}")
        return False
    
    if not os.access(path, os.R_OK):
        print(f"❌ File non leggibile: {file_path}")
        return False
    
    return True

def generate_hash(data: str, algorithm: str = "md5") -> str:
    """
    Generate hash of a string
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm (md5, sha1, sha256)
    
    Returns:
        Hash string
    """
    if algorithm == "md5":
        return hashlib.md5(data.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(data.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(data.encode()).hexdigest()
    else:
        raise ValueError(f"Algorithm not supported: {algorithm}")

def calculate_speed(processed: int, elapsed: float) -> float:
    """
    Calculate processing speed
    
    Args:
        processed: Number of items processed
        elapsed: Time elapsed in seconds
    
    Returns:
        Items per second
    """
    return processed / elapsed if elapsed > 0 else 0.0

def human_readable_time(seconds: float) -> str:
    """
    Convert seconds to human readable time
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f} secondi"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minuti"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} ore"
    else:
        days = seconds / 86400
        return f"{days:.1f} giorni"

def load_config(config_file: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from file
    
    Args:
        config_file: Configuration file path (JSON or YAML)
    
    Returns:
        Configuration dictionary
    """
    path = Path(config_file)
    
    if not path.exists():
        return {}
    
    with open(path, 'r', encoding='utf-8') as f:
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")

def save_config(config: Dict[str, Any], config_file: Union[str, Path]) -> None:
    """
    Save configuration to file
    
    Args:
        config: Configuration dictionary
        config_file: Output file path
    """
    path = Path(config_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        if path.suffix in ['.yaml', '.yml']:
            yaml.dump(config, f, default_flow_style=False)
        elif path.suffix == '.json':
            json.dump(config, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")

class ProgressBar:
    """
    Simple progress bar for command line
    """
    
    def __init__(self, total: int, prefix: str = "", length: int = 50):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.current = 0
        self.start_time = time.time()
        
    def update(self, current: Optional[int] = None):
        """Update progress bar"""
        if current is not None:
            self.current = current
        else:
            self.current += 1
        
        if self.current > self.total:
            self.current = self.total
        
        self._render()
    
    def _render(self):
        """Render the progress bar"""
        progress = self.current / self.total
        filled = int(self.length * progress)
        bar = '█' * filled + '░' * (self.length - filled)
        
        elapsed = time.time() - self.start_time
        speed = calculate_speed(self.current, elapsed)
        
        print(
            f'\r{self.prefix} |{bar}| {self.current:,}/{self.total:,} '
            f'({progress*100:.1f}%) - {speed:.0f}/s',
            end=''
        )
        
        if self.current >= self.total:
            print()

class MemoryOptimizer:
    """
    Utility for memory optimization
    """
    
    @staticmethod
    def should_use_chunked_processing(file_size: int) -> bool:
        """
        Determine if chunked processing is needed
        
        Args:
            file_size: Size of file in bytes
        
        Returns:
            True if chunked processing is recommended
        """
        mem = get_memory_usage()
        available_memory = mem['available']
        
        # Usa chunked se il file è > 50% della RAM disponibile
        return file_size > (available_memory * 0.5)
    
    @staticmethod
    def get_optimal_chunk_size(file_size: int) -> int:
        """
        Calculate optimal chunk size
        
        Args:
            file_size: Size of file in bytes
        
        Returns:
            Optimal chunk size in bytes
        """
        mem = get_memory_usage()
        available_memory = mem['available']
        
        # Usa al massimo 10% della RAM per chunk
        max_chunk = int(available_memory * 0.1)
        
        # Limite minimo e massimo
        min_chunk = 1024 * 1024  # 1MB
        max_chunk = 100 * 1024 * 1024  # 100MB
        
        chunk = min(max_chunk, max(min_chunk, file_size // 10))
        return chunk

if __name__ == "__main__":
    # Test delle utility
    print("📊 Test delle utility:")
    print(f"Memory usage: {format_bytes(get_memory_usage()['used'])}")
    
    # Test progress bar
    pb = ProgressBar(100, prefix="Test")
    for i in range(100):
        time.sleep(0.01)
        pb.update()