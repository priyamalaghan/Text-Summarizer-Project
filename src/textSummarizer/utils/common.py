import os
from box.exceptions import BoxValueError #BoxValueError is raised when there are issues with the values passed to a Box object.
import yaml #Imports the PyYAML library, used to load or dump YAML data
from textSummarizer.logging import logger
from ensure import ensure_annotations #Imports a decorator from the ensure package that enforces function annotations at runtime (e.g., makes sure arguments and return types match the function signature).
from box import ConfigBox #Imports ConfigBox from python-box. This allows dictionary access using dot notation: config.key instead of config['key']
from pathlib import Path #Imports Path from pathlib, a modern way to handle filesystem paths that’s OS-independent.
from typing import Any #Any is part of the typing module in Python and is used to indicate that any type is acceptable for a variable, function argument, or return type.

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox: #returns ConfigBox type output
    """reads yaml file and returns
    Args:
        path_to_yaml (str): path like input
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        #logger.error(f"Failed to read YAML file '{path_to_yaml}' : {e}")
        #raise
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories
    Args:
        path_to_directories (list) : list of path of directories
        verbose (bool, optional): If True, logs the creation of each directory. Defaults to True
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")

@ensure_annotations
def get_size(path:Path) -> str:
    """get size in KB
    Args:
        path (Path): path of the file
    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"
