"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       COLOR SORTING TASK PROMPTS                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


PROMPTS = {
    "default": [
        "The image shows scattered colored blocks and empty containers. Move each block into the container that matches its color. Arrange the blocks neatly inside the containers.",
        "Sort the colored blocks by moving each one into the container of the same color. Organize them neatly in a grid pattern inside each container.",
        "Categorize the scattered colored blocks by placing each block into its matching colored container. Arrange them in an orderly manner.",
    ],
    "two_colors": [
        "The image shows blue and yellow blocks scattered around two containers. Sort the blocks by placing each one in the container that matches its color.",
        "Move all the colored blocks into their corresponding containers - blue blocks go in the blue container, yellow blocks go in the yellow container.",
    ],
    "multi_colors": [
        "Sort the multi-colored blocks by placing each one into the container that matches its color. Arrange them neatly inside.",
        "The image shows blocks of various colors and multiple containers. Move each block into the container of matching color.",
    ],
}


def get_prompt(task_type: str = "default") -> str:
    """Select a random prompt for the given task type."""
    prompts = PROMPTS.get(task_type, PROMPTS["default"])
    return random.choice(prompts)


def get_all_prompts(task_type: str = "default") -> list[str]:
    """Get all prompts for a given task type."""
    return PROMPTS.get(task_type, PROMPTS["default"])
