import logging
import sys
import json
import yaml
from typing import Dict, List

logging_level_mapping = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Sets up and returns a configured logger."""
    # Prevent multiple handlers if called multiple times
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger # Logger already configured

    logger.setLevel(level)

    # Create console handler and set level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger

def get_logging_level(log_level: str) -> int:
    """Get logging level from string"""
    return logging_level_mapping.get(log_level, logging.INFO)


def load_yaml_config(file_path: str) -> dict:
    """Load yaml config"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def load_json(file_path: str) -> dict:
    """Load json file"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_json(
    data: Dict | List, 
    file_path: str, 
    indent: int = 4, 
    ensure_ascii: bool = False
) -> None:
    """Save json file"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)