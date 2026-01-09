"""
Color Sorting Task Implementation.

Task: Move colored blocks into matching color containers.
"""

from .config import TaskConfig
from .generator import TaskGenerator
from .prompts import get_prompt

__all__ = ["TaskConfig", "TaskGenerator", "get_prompt"]
