"""
Size Sorting Task - src module

Exports:
    - TaskConfig: Configuration class for the task
    - TaskGenerator: Generator class for creating task pairs
    - get_prompt: Function to get task prompts
"""

from .config import TaskConfig
from .generator import TaskGenerator
from .prompts import get_prompt, get_all_prompts

__all__ = [
    "TaskConfig",
    "TaskGenerator",
    "get_prompt",
    "get_all_prompts",
]
