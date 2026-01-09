"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       COLOR SORTING TASK CONFIGURATION                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """
    Color sorting task configuration.
    
    Inherited from GenerationConfig:
        - num_samples: int
        - domain: str
        - difficulty: Optional[str]
        - random_seed: Optional[int]
        - output_dir: Path
        - image_size: tuple[int, int]
    """
    
    # Override defaults
    domain: str = Field(default="color_sorting")
    image_size: tuple[int, int] = Field(default=(600, 400))
    
    # Video settings
    generate_videos: bool = Field(default=True, description="Whether to generate ground truth videos")
    video_fps: int = Field(default=10, description="Video frame rate")
    
    # Task-specific settings
    num_colors: int = Field(default=2, description="Number of color categories (2-6)")
    items_per_color: int = Field(default=4, description="Number of blocks per color")
    block_size: int = Field(default=25, description="Size of each block in pixels")
