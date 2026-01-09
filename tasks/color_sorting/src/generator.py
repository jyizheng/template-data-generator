"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       COLOR SORTING TASK GENERATOR                            ║
║                                                                               ║
║  Task: Move colored blocks into matching color containers                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
from typing import Optional
from pathlib import Path
import tempfile
from PIL import Image, ImageDraw

from core import BaseGenerator, TaskPair
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

AVAILABLE_COLORS = {
    "yellow": (255, 215, 0),
    "blue": (0, 100, 255),
    "red": (220, 60, 60),
    "green": (60, 180, 60),
    "purple": (150, 80, 200),
    "orange": (255, 140, 0),
}


class TaskGenerator(BaseGenerator):
    """
    Generator for color sorting task pairs.
    
    Generates image pairs showing:
    - Input: Scattered colored blocks with empty containers
    - Output: Blocks sorted into matching color containers
    """
    
    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.width, self.height = config.image_size
        
        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(
                fps=config.video_fps,
                output_format="mp4"
            )
    
    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one color sorting task pair."""
        
        # Generate task data
        task_data = self._generate_task_data()
        
        # Render input and output images
        first_image = self._render_frame(task_data, state="input")
        final_image = self._render_frame(task_data, state="output")
        
        # Generate video (optional)
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(task_id, task_data)
        
        # Get prompt
        prompt = get_prompt(task_data["task_type"])
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path
        )
    
    def _generate_task_data(self) -> dict:
        """Generate task data including colors, items, and positions."""
        num_colors = self.config.num_colors
        items_per_color = self.config.items_per_color
        block_size = self.config.block_size
        
        # Select random colors
        color_names = list(AVAILABLE_COLORS.keys())
        selected_names = random.sample(color_names, min(num_colors, len(color_names)))
        selected_colors = {name: AVAILABLE_COLORS[name] for name in selected_names}
        
        # Generate containers
        bins = self._generate_bins(selected_colors)
        
        # Generate items
        items = self._generate_items(selected_colors, items_per_color, block_size)
        
        # Calculate sorted positions
        sorted_positions = self._get_sorted_positions(items, bins, selected_colors)
        
        # Determine task type for prompt
        if num_colors == 2:
            task_type = "two_colors"
        elif num_colors > 2:
            task_type = "multi_colors"
        else:
            task_type = "default"
        
        return {
            "selected_colors": selected_colors,
            "bins": bins,
            "items": items,
            "sorted_positions": sorted_positions,
            "block_size": block_size,
            "task_type": task_type,
        }
    
    def _generate_bins(self, selected_colors: dict) -> list:
        """Generate container positions."""
        bins = []
        color_names = list(selected_colors.keys())
        
        bin_width = 150
        bin_height = 100
        
        total_bin_width = len(color_names) * bin_width
        spacing = (self.width - total_bin_width) // (len(color_names) + 1)
        bin_y = self.height - bin_height - 50
        
        for i, color_name in enumerate(color_names):
            bin_x = spacing + i * (bin_width + spacing)
            bins.append({
                "rect": (bin_x, bin_y, bin_width, bin_height),
                "color": color_name
            })
        
        return bins
    
    def _generate_items(self, selected_colors: dict, items_per_color: int, block_size: int) -> list:
        """Generate scattered items."""
        items = []
        
        for color_name, color_val in selected_colors.items():
            for i in range(items_per_color):
                rand_x = random.randint(50, self.width - 50)
                rand_y = random.randint(50, self.height // 2 - 30)
                
                items.append({
                    "color_name": color_name,
                    "color_val": color_val,
                    "size": block_size,
                    "start_pos": (rand_x, rand_y),
                    "id": f"{color_name}_{i}"
                })
        
        return items
    
    def _get_sorted_positions(self, items: list, bins: list, selected_colors: dict) -> dict:
        """Calculate sorted positions inside containers."""
        target_positions = {}
        counters = {name: 0 for name in selected_colors.keys()}
        
        for item in items:
            color_name = item["color_name"]
            idx = counters[color_name]
            counters[color_name] += 1
            
            bin_data = next(b for b in bins if b["color"] == color_name)
            bx, by, bw, bh = bin_data["rect"]
            
            cols = 2
            row = idx // cols
            col = idx % cols
            
            padding_x = bw // 3
            padding_y = bh // 3
            
            target_x = bx + padding_x * (col + 1)
            target_y = by + padding_y * (row + 1) - 10
            
            target_positions[item["id"]] = (int(target_x), int(target_y))
        
        return target_positions
    
    def _render_frame(self, task_data: dict, state: str = "input") -> Image.Image:
        """Render a frame for the given state."""
        canvas = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        selected_colors = task_data["selected_colors"]
        bins = task_data["bins"]
        items = task_data["items"]
        sorted_positions = task_data["sorted_positions"]
        
        # Draw containers
        for b in bins:
            bx, by, bw, bh = b["rect"]
            color = selected_colors[b["color"]]
            draw.rectangle([bx, by, bx + bw, by + bh], outline=color, width=4)
        
        # Draw items
        for item in items:
            color = item["color_val"]
            size = item["size"]
            
            if state == "input":
                cx, cy = item["start_pos"]
            else:
                cx, cy = sorted_positions[item["id"]]
            
            half = size // 2
            draw.rectangle([cx - half, cy - half, cx + half, cy + half], fill=color)
            draw.rectangle([cx - half, cy - half, cx + half, cy + half], outline=(50, 50, 50), width=1)
        
        return canvas
    
    def _generate_video(self, task_id: str, task_data: dict) -> Optional[str]:
        """Generate animation video."""
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"
        
        frames = self._create_animation_frames(task_data)
        
        result = self.video_generator.create_video_from_frames(frames, video_path)
        return str(result) if result else None
    
    def _create_animation_frames(self, task_data: dict, hold_frames: int = 10, transition_frames: int = 20) -> list:
        """Create animation frames."""
        frames = []
        
        items = task_data["items"]
        sorted_positions = task_data["sorted_positions"]
        
        start_positions = {item["id"]: item["start_pos"] for item in items}
        
        # Hold initial frame
        initial_frame = self._render_frame(task_data, state="input")
        for _ in range(hold_frames):
            frames.append(initial_frame)
        
        # Transition frames
        for i in range(transition_frames):
            progress = i / (transition_frames - 1) if transition_frames > 1 else 1.0
            frame = self._render_interpolated_frame(task_data, start_positions, sorted_positions, progress)
            frames.append(frame)
        
        # Hold final frame
        final_frame = self._render_frame(task_data, state="output")
        for _ in range(hold_frames):
            frames.append(final_frame)
        
        return frames
    
    def _render_interpolated_frame(self, task_data: dict, start_positions: dict, end_positions: dict, progress: float) -> Image.Image:
        """Render frame with interpolated positions."""
        canvas = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        selected_colors = task_data["selected_colors"]
        bins = task_data["bins"]
        items = task_data["items"]
        
        # Draw containers
        for b in bins:
            bx, by, bw, bh = b["rect"]
            color = selected_colors[b["color"]]
            draw.rectangle([bx, by, bx + bw, by + bh], outline=color, width=4)
        
        # Draw items at interpolated positions
        for item in items:
            item_id = item["id"]
            color = item["color_val"]
            size = item["size"]
            
            sx, sy = start_positions[item_id]
            ex, ey = end_positions[item_id]
            
            cx = int(sx + (ex - sx) * progress)
            cy = int(sy + (ey - sy) * progress)
            
            half = size // 2
            draw.rectangle([cx - half, cy - half, cx + half, cy + half], fill=color)
            draw.rectangle([cx - half, cy - half, cx + half, cy + half], outline=(50, 50, 50), width=1)
        
        return canvas
