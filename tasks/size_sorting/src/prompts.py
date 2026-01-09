"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       SIZE SORTING TASK PROMPTS                               ║
║                                                                               ║
║  Prompt templates for size sorting task                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = {
    "default": [
        "Sort the scattered bars from shortest to tallest. Align them horizontally at the bottom.",
        "Arrange the colorful bars in ascending order of height, placing them side by side on the baseline.",
        "Organize the randomly placed bars by their height, from smallest to largest, aligned at the bottom.",
        "Reorder the bars by size, placing the shortest on the left and tallest on the right, all aligned at the bottom.",
    ],
    "ascending": [
        "Sort the bars from shortest to tallest and align them at the bottom baseline.",
        "Arrange the scattered rectangular bars in ascending height order along the bottom.",
        "Order the bars from smallest to largest height, placing them side by side at the baseline.",
        "Organize these bars by height from left to right, shortest first, aligned at the bottom.",
    ],
    "descending": [
        "Sort the bars from tallest to shortest and align them at the bottom baseline.",
        "Arrange the scattered rectangular bars in descending height order along the bottom.",
        "Order the bars from largest to smallest height, placing them side by side at the baseline.",
        "Organize these bars by height from left to right, tallest first, aligned at the bottom.",
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
