#!/usr/bin/env python3
"""
Advanced logging utilities for Digimundo.
This module centralizes configuration of per-module or per-Digimon loggers.
"""
import logging
import os
from datetime import datetime

def get_logger(name: str, log_dir: str = "logs/digimundo", level: int = logging.INFO) -> logging.Logger:
    """
    Returns a logger that writes messages to a file in the given directory. The file is rotated daily.

    :param name: Name of the logger (e.g., digimon or module).
    :param log_dir: Base directory where logs will be stored.
    :param level: Logging level (default: INFO).
    :return: Configured Logger instance.
    """
    # Determine the directory for this logger.
    date_str = datetime.now().strftime("%Y-%m-%d")
    full_log_dir = os.path.join(log_dir, name)
    os.makedirs(full_log_dir, exist_ok=True)
    file_path = os.path.join(full_log_dir, f"{name}_{date_str}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicate logs.
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def setup_loggers(names, log_dir: str = "logs/digimundo", level: int = logging.INFO):
    """
    Creates multiple loggers for each name (Digimon, module, etc.) in subdirectories.
    Returns a dictionary mapping name to logger instance.

    :param names: Iterable of logger names to create.
    :param log_dir: Base directory where all logs will be stored.
    :param level: Logging level to assign to each logger.
    :return: Dictionary of {name: Logger}.
    """
    return {name: get_logger(name, log_dir, level) for name in names}
