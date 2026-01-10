"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   ANIMAL SIZE SORTING TASK CONFIGURATION                      ║
║                                                                               ║
║  Configuration classes for animal size sorting task generation                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """Configuration for animal size sorting task generation."""
    
    # Domain identifier
    domain: str = "O-5_animal_size_sorting"
    
    # Image settings
    image_size: tuple[int, int] = Field(
        default=(800, 500),
        description="Size of generated images (width, height)"
    )
    
    # Task-specific settings
    num_animals: int = Field(
        default=5,
        ge=3,
        le=6,
        description="Number of animals to sort (3-6)"
    )
    
    min_size: int = Field(
        default=30,
        ge=20,
        le=50,
        description="Minimum animal size in pixels"
    )
    
    max_size: int = Field(
        default=80,
        ge=60,
        le=120,
        description="Maximum animal size in pixels"
    )
    
    sort_order: str = Field(
        default="ascending",
        pattern="^(ascending|descending)$",
        description="Sort order: 'ascending' (smallest to largest) or 'descending' (largest to smallest)"
    )
    
    # Video settings
    generate_videos: bool = Field(
        default=False,
        description="Whether to generate ground truth videos"
    )
    
    video_fps: int = Field(
        default=10,
        ge=5,
        le=30,
        description="Frames per second for generated videos"
    )
