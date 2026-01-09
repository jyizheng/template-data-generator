"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       PATH PLANNING TASK PROMPTS                              ║
║                                                                               ║
║  Prompt templates for path planning task                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = {
    "default": [
        "Draw a continuous line from the red start circle to the green goal circle, avoiding all black obstacles.",
        "Find and draw the shortest path from the red circle to the green circle without crossing any black obstacles.",
        "Navigate from the red starting point to the green destination, plotting a path that avoids all black walls.",
        "Plan and draw a route from the red origin to the green target, steering clear of all obstacles.",
    ],
    "maze": [
        "Solve the maze by drawing a path from the red start to the green goal, avoiding all black walls.",
        "Find your way through the maze from red to green, drawing a continuous line that doesn't cross obstacles.",
        "Navigate through this maze from the red circle to the green circle without hitting any walls.",
    ],
    "navigation": [
        "Plan a route from the red origin to the green destination that avoids all blocked cells.",
        "Draw a navigation path from start (red) to goal (green), steering clear of all obstacles (black).",
        "Find the optimal path from the red point to the green point, avoiding all black obstacles.",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
#  PROMPT SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def get_prompt(task_type: str = "default") -> str:
    """
    Select a random prompt for the given task type.
    
    Args:
        task_type: Type of task ("default", "maze", "navigation")
        
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
