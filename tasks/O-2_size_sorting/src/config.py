"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       SIZE SORTING TASK CONFIGURATION                         ║
║                                                                               ║
║  Configuration classes for size sorting task generation                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core.schemas import GenerationConfig


class TaskConfig(GenerationConfig):
    """Configuration for size sorting task generation."""
    
    # Domain identifier
    domain: str = "O-2_size_sorting"
    
    # Image settings
    image_size: tuple[int, int] = Field(
        default=(800, 400),
        description="Size of generated images (width, height)"
    )
    
    # Task-specific settings
    num_bars: int = Field(
        default=7,
        ge=3,
        le=15,
        description="Number of bars to sort"
    )
    
    bar_width: int = Field(
        default=40,
        ge=20,
        le=80,
        description="Width of each bar in pixels"
    )
    
    min_height: int = Field(
        default=50,
        ge=30,
        le=150,
        description="Minimum bar height in pixels"
    )
    
    max_height: int = Field(
        default=250,
        ge=150,
        le=350,
        description="Maximum bar height in pixels"
    )
    
    sort_order: str = Field(
        default="ascending",
        pattern="^(ascending|descending)$",
        description="Sort order: 'ascending' (shortest to tallest) or 'descending' (tallest to shortest)"
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
