"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       PATH PLANNING TASK CONFIGURATION                        ║
║                                                                               ║
║  Configuration classes for path planning task generation                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core.schemas import GenerationConfig


class TaskConfig(GenerationConfig):
    """Configuration for path planning task generation."""
    
    # Domain identifier
    domain: str = "path_planning"
    
    # Grid settings
    grid_width: int = Field(
        default=15,
        ge=5,
        le=30,
        description="Number of columns in the grid"
    )
    
    grid_height: int = Field(
        default=10,
        ge=5,
        le=20,
        description="Number of rows in the grid"
    )
    
    cell_size: int = Field(
        default=40,
        ge=20,
        le=80,
        description="Size of each cell in pixels"
    )
    
    obstacle_density: float = Field(
        default=0.25,
        ge=0.1,
        le=0.5,
        description="Percentage of cells that are obstacles (0.1-0.5)"
    )
    
    # Image size is calculated from grid dimensions
    @property
    def image_size(self) -> tuple[int, int]:
        """Calculate image size from grid dimensions."""
        return (self.grid_width * self.cell_size, self.grid_height * self.cell_size)
    
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
