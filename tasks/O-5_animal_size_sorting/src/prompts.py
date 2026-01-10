"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     ANIMAL SIZE SORTING TASK PROMPTS                          ║
║                                                                               ║
║  Prompt templates for animal size sorting task                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = {
    "default": [
        "Sort the scattered animal faces by size from smallest to largest. Align them horizontally at the bottom.",
        "Arrange the animals in ascending order of size, placing them side by side on the baseline.",
        "Organize the randomly placed animal faces by their size, from the smallest on the left to the largest on the right.",
        "Reorder the animals by size, placing the smallest first and largest last, all aligned at the bottom line.",
    ],
    "ascending": [
        "Sort the animal faces from smallest to largest and align them at the bottom baseline.",
        "Arrange the scattered animals in ascending size order along the bottom.",
        "Order the animals from smallest to largest, placing them side by side at the baseline.",
        "Line up these animals by size from left to right, smallest first, aligned at the bottom.",
    ],
    "descending": [
        "Sort the animal faces from largest to smallest and align them at the bottom baseline.",
        "Arrange the scattered animals in descending size order along the bottom.",
        "Order the animals from largest to smallest, placing them side by side at the baseline.",
        "Line up these animals by size from left to right, largest first, aligned at the bottom.",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
#  PROMPT SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def get_prompt(task_type: str = "default") -> str:
    """
    Select a random prompt for the given task type.
    
    Args:
        task_type: Type of task ("default", "ascending", "descending")
        
    Returns:
        A randomly selected prompt string
    """
    prompts = PROMPTS.get(task_type, PROMPTS["default"])
    return random.choice(prompts)


def get_all_prompts(task_type: str = "default") -> list[str]:
    """
    Get all prompts for a given task type.
    
    Args:
        task_type: Type of task
        
    Returns:
        List of all prompts for that type
    """
    return PROMPTS.get(task_type, PROMPTS["default"])
