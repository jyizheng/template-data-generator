"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ANIMAL SIZE SORTING TASK GENERATOR                         ║
║                                                                               ║
║  Combines size sorting with animal faces                                      ║
║  Task: Sort scattered animals by size from smallest to largest                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
from typing import Optional, Any, Tuple
from pathlib import Path
import tempfile

from PIL import Image, ImageDraw

from core import BaseGenerator, TaskPair
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


# ══════════════════════════════════════════════════════════════════════════════
#  ANIMAL TYPES AND COLORS
# ══════════════════════════════════════════════════════════════════════════════

ANIMAL_TYPES = ["cat", "dog", "rabbit", "bear", "panda", "fox"]

ANIMAL_COLORS = {
    "cat": (255, 180, 100),      # Orange cat
    "dog": (180, 140, 100),      # Brown dog
    "rabbit": (255, 200, 220),   # Pink rabbit
    "bear": (160, 120, 80),      # Brown bear
    "panda": (240, 240, 240),    # White panda
    "fox": (255, 140, 60),       # Orange fox
}


# ══════════════════════════════════════════════════════════════════════════════
#  ANIMAL DRAWING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def draw_cat(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, color):
    """Draw a cat face with pointy ears."""
    cx, cy = center
    
    # Ears first (behind face)
    ear_points_l = [(cx - size*0.8, cy - size*0.5), 
                   (cx - size*0.4, cy - size*1.3), 
                   (cx - size*0.2, cy - size*0.6)]
    draw.polygon(ear_points_l, fill=color, outline=(50, 50, 50), width=1)
    ear_points_r = [(cx + size*0.8, cy - size*0.5), 
                   (cx + size*0.4, cy - size*1.3), 
                   (cx + size*0.2, cy - size*0.6)]
    draw.polygon(ear_points_r, fill=color, outline=(50, 50, 50), width=1)
    # Face
    draw.ellipse([cx - size, cy - size*0.8, cx + size, cy + size*0.9], 
                fill=color, outline=(50, 50, 50), width=1)
    # Eyes
    draw.ellipse([cx - size*0.5, cy - size*0.2, cx - size*0.2, cy + size*0.1], fill=(50, 50, 50))
    draw.ellipse([cx + size*0.2, cy - size*0.2, cx + size*0.5, cy + size*0.1], fill=(50, 50, 50))
    # Nose
    draw.polygon([(cx, cy + size*0.1), (cx - size*0.15, cy + size*0.3), 
                 (cx + size*0.15, cy + size*0.3)], fill=(255, 150, 150))
    # Whiskers
    draw.line([(cx - size*0.2, cy + size*0.3), (cx - size*0.9, cy + size*0.1)], fill=(50, 50, 50), width=1)
    draw.line([(cx - size*0.2, cy + size*0.4), (cx - size*0.9, cy + size*0.4)], fill=(50, 50, 50), width=1)
    draw.line([(cx + size*0.2, cy + size*0.3), (cx + size*0.9, cy + size*0.1)], fill=(50, 50, 50), width=1)
    draw.line([(cx + size*0.2, cy + size*0.4), (cx + size*0.9, cy + size*0.4)], fill=(50, 50, 50), width=1)


def draw_dog(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, color):
    """Draw a dog face with floppy ears."""
    cx, cy = center
    
    # Ears first (behind face)
    draw.ellipse([cx - size*1.3, cy - size*0.6, cx - size*0.5, cy + size*0.5], 
                fill=color, outline=(50, 50, 50), width=1)
    draw.ellipse([cx + size*0.5, cy - size*0.6, cx + size*1.3, cy + size*0.5], 
                fill=color, outline=(50, 50, 50), width=1)
    # Face
    draw.ellipse([cx - size, cy - size*0.7, cx + size, cy + size*0.9], 
                fill=color, outline=(50, 50, 50), width=1)
    # Eyes
    draw.ellipse([cx - size*0.5, cy - size*0.3, cx - size*0.2, cy], fill=(50, 50, 50))
    draw.ellipse([cx + size*0.2, cy - size*0.3, cx + size*0.5, cy], fill=(50, 50, 50))
    # Big nose
    draw.ellipse([cx - size*0.25, cy + size*0.1, cx + size*0.25, cy + size*0.45], fill=(50, 50, 50))
    # Tongue
    draw.ellipse([cx - size*0.15, cy + size*0.45, cx + size*0.15, cy + size*0.8], fill=(255, 150, 150))


def draw_rabbit(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, color):
    """Draw a rabbit face with long ears."""
    cx, cy = center
    
    # Long ears first
    draw.ellipse([cx - size*0.6, cy - size*1.8, cx - size*0.1, cy - size*0.3], 
                fill=color, outline=(50, 50, 50), width=1)
    draw.ellipse([cx - size*0.5, cy - size*1.6, cx - size*0.2, cy - size*0.5], 
                fill=(255, 180, 180))
    draw.ellipse([cx + size*0.1, cy - size*1.8, cx + size*0.6, cy - size*0.3], 
                fill=color, outline=(50, 50, 50), width=1)
    draw.ellipse([cx + size*0.2, cy - size*1.6, cx + size*0.5, cy - size*0.5], 
                fill=(255, 180, 180))
    # Face
    draw.ellipse([cx - size*0.9, cy - size*0.5, cx + size*0.9, cy + size*0.9], 
                fill=color, outline=(50, 50, 50), width=1)
    # Eyes
    draw.ellipse([cx - size*0.5, cy - size*0.1, cx - size*0.2, cy + size*0.2], fill=(50, 50, 50))
    draw.ellipse([cx + size*0.2, cy - size*0.1, cx + size*0.5, cy + size*0.2], fill=(50, 50, 50))
    # Nose
    draw.ellipse([cx - size*0.12, cy + size*0.25, cx + size*0.12, cy + size*0.45], fill=(255, 150, 150))
    # Teeth
    draw.rectangle([cx - size*0.1, cy + size*0.45, cx + size*0.1, cy + size*0.7], 
                  fill=(255, 255, 255), outline=(50, 50, 50))
    draw.line([(cx, cy + size*0.45), (cx, cy + size*0.7)], fill=(50, 50, 50), width=1)


def draw_bear(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, color):
    """Draw a bear face with round ears."""
    cx, cy = center
    
    # Round ears first
    draw.ellipse([cx - size*1.1, cy - size*1.2, cx - size*0.4, cy - size*0.5], 
                fill=color, outline=(50, 50, 50), width=1)
    draw.ellipse([cx + size*0.4, cy - size*1.2, cx + size*1.1, cy - size*0.5], 
                fill=color, outline=(50, 50, 50), width=1)
    # Face
    draw.ellipse([cx - size, cy - size*0.8, cx + size, cy + size*0.9], 
                fill=color, outline=(50, 50, 50), width=1)
    # Muzzle area (lighter)
    lighter_color = tuple(min(255, c + 40) for c in color)
    draw.ellipse([cx - size*0.5, cy + size*0.1, cx + size*0.5, cy + size*0.7], fill=lighter_color)
    # Eyes
    draw.ellipse([cx - size*0.5, cy - size*0.3, cx - size*0.2, cy], fill=(50, 50, 50))
    draw.ellipse([cx + size*0.2, cy - size*0.3, cx + size*0.5, cy], fill=(50, 50, 50))
    # Nose
    draw.ellipse([cx - size*0.2, cy + size*0.15, cx + size*0.2, cy + size*0.4], fill=(50, 50, 50))
    # Smile
    draw.arc([cx - size*0.25, cy + size*0.3, cx + size*0.25, cy + size*0.55], 
            start=0, end=180, fill=(50, 50, 50), width=2)


def draw_panda(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, color):
    """Draw a panda face with black ear patches."""
    cx, cy = center
    
    # Round ears (black)
    draw.ellipse([cx - size*1.1, cy - size*1.2, cx - size*0.4, cy - size*0.5], 
                fill=(30, 30, 30), outline=(20, 20, 20), width=1)
    draw.ellipse([cx + size*0.4, cy - size*1.2, cx + size*1.1, cy - size*0.5], 
                fill=(30, 30, 30), outline=(20, 20, 20), width=1)
    # Face (white)
    draw.ellipse([cx - size, cy - size*0.8, cx + size, cy + size*0.9], 
                fill=color, outline=(50, 50, 50), width=1)
    # Eye patches (black)
    draw.ellipse([cx - size*0.7, cy - size*0.4, cx - size*0.1, cy + size*0.2], fill=(30, 30, 30))
    draw.ellipse([cx + size*0.1, cy - size*0.4, cx + size*0.7, cy + size*0.2], fill=(30, 30, 30))
    # Eyes (white dots)
    draw.ellipse([cx - size*0.5, cy - size*0.15, cx - size*0.3, cy + size*0.05], fill=(255, 255, 255))
    draw.ellipse([cx + size*0.3, cy - size*0.15, cx + size*0.5, cy + size*0.05], fill=(255, 255, 255))
    # Nose
    draw.ellipse([cx - size*0.15, cy + size*0.25, cx + size*0.15, cy + size*0.45], fill=(30, 30, 30))


def draw_fox(draw: ImageDraw.Draw, center: Tuple[int, int], size: int, color):
    """Draw a fox face with pointy ears and white muzzle."""
    cx, cy = center
    
    # Pointy ears
    ear_points_l = [(cx - size*0.9, cy - size*0.4), 
                   (cx - size*0.5, cy - size*1.4), 
                   (cx - size*0.1, cy - size*0.5)]
    draw.polygon(ear_points_l, fill=color, outline=(50, 50, 50), width=1)
    # Inner ear
    inner_ear_l = [(cx - size*0.75, cy - size*0.5), 
                  (cx - size*0.5, cy - size*1.1), 
                  (cx - size*0.25, cy - size*0.55)]
    draw.polygon(inner_ear_l, fill=(30, 30, 30))
    
    ear_points_r = [(cx + size*0.9, cy - size*0.4), 
                   (cx + size*0.5, cy - size*1.4), 
                   (cx + size*0.1, cy - size*0.5)]
    draw.polygon(ear_points_r, fill=color, outline=(50, 50, 50), width=1)
    inner_ear_r = [(cx + size*0.75, cy - size*0.5), 
                  (cx + size*0.5, cy - size*1.1), 
                  (cx + size*0.25, cy - size*0.55)]
    draw.polygon(inner_ear_r, fill=(30, 30, 30))
    
    # Face
    draw.ellipse([cx - size, cy - size*0.7, cx + size, cy + size*0.9], 
                fill=color, outline=(50, 50, 50), width=1)
    # White muzzle area
    draw.ellipse([cx - size*0.6, cy + size*0.1, cx + size*0.6, cy + size*0.85], fill=(255, 255, 255))
    # Eyes
    draw.ellipse([cx - size*0.5, cy - size*0.25, cx - size*0.2, cy + size*0.05], fill=(50, 50, 50))
    draw.ellipse([cx + size*0.2, cy - size*0.25, cx + size*0.5, cy + size*0.05], fill=(50, 50, 50))
    # Nose
    draw.ellipse([cx - size*0.15, cy + size*0.2, cx + size*0.15, cy + size*0.4], fill=(30, 30, 30))


def draw_animal(draw: ImageDraw.Draw, animal_type: str, 
                center: Tuple[int, int], size: int, color):
    """Draw an animal face based on type."""
    drawers = {
        "cat": draw_cat,
        "dog": draw_dog,
        "rabbit": draw_rabbit,
        "bear": draw_bear,
        "panda": draw_panda,
        "fox": draw_fox,
    }
    if animal_type in drawers:
        drawers[animal_type](draw, center, size, color)


# ══════════════════════════════════════════════════════════════════════════════
#  ANIMAL SIZE SORTING TASK
# ══════════════════════════════════════════════════════════════════════════════

class AnimalSizeSortingTask:
    """
    Animal size sorting task.
    
    Generates input/output image pairs showing:
    - Input: Scattered animal faces of different sizes
    - Output: Animals sorted by size and aligned at baseline
    """
    
    def __init__(
        self,
        width: int = 800,
        height: int = 500,
        num_animals: int = 5,
        min_size: int = 30,
        max_size: int = 80,
        sort_order: str = "ascending"
    ):
        self.width = width
        self.height = height
        self.num_animals = min(num_animals, len(ANIMAL_TYPES))
        self.min_size = min_size
        self.max_size = max_size
        self.sort_order = sort_order
        
        # Generate animal data
        self.data = self._generate_data()
    
    def _generate_data(self) -> list:
        """Generate animals with random sizes, types, and initial positions."""
        data = []
        
        # Select random animal types (no duplicates)
        selected_animals = random.sample(ANIMAL_TYPES, self.num_animals)
        
        # Generate unique random sizes
        sizes = set()
        while len(sizes) < self.num_animals:
            sizes.add(random.randint(self.min_size, self.max_size))
        sizes = list(sizes)
        random.shuffle(sizes)
        
        for i, (animal_type, size) in enumerate(zip(selected_animals, sizes)):
            color = ANIMAL_COLORS.get(animal_type, (200, 200, 200))
            
            # Add slight color variation
            color = tuple(
                max(0, min(255, c + random.randint(-20, 20)))
                for c in color
            )
            
            # Random initial position (scattered) - account for animal size + ears
            margin = size * 2  # Extra margin for ears
            rand_x = random.randint(margin, self.width - margin)
            rand_y = random.randint(margin, self.height - margin - 50)
            
            data.append({
                "animal_type": animal_type,
                "size": size,
                "color": color,
                "input_pos": (rand_x, rand_y)
            })
        
        return data
    
    def render(self, state: str = "input") -> Image.Image:
        """
        Render the task state.
        
        Args:
            state: "input" for scattered animals, "output" for sorted animals
            
        Returns:
            PIL Image of the rendered state
        """
        # Create white background
        canvas = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        # Baseline position (bottom area)
        baseline_y = self.height - 80
        
        # Prepare data for rendering
        render_data = self.data.copy()
        
        if state == "output":
            # Sort by size
            reverse = (self.sort_order == "descending")
            render_data.sort(key=lambda x: x["size"], reverse=reverse)
            
            # Draw baseline (visual guide)
            draw.line([(30, baseline_y), (self.width - 30, baseline_y)], 
                     fill=(200, 200, 200), width=2)
        
        # Calculate positions for output state
        if state == "output":
            # Calculate total width needed
            gap = 30
            total_width = sum(item["size"] * 2.5 for item in render_data) + (len(render_data) - 1) * gap
            start_x = (self.width - total_width) // 2
            
            current_x = start_x
            for item in render_data:
                size = item["size"]
                # Center of animal
                cx = current_x + size * 1.25
                cy = baseline_y - size * 1.2  # Position above baseline
                item["output_pos"] = (cx, cy)
                current_x += size * 2.5 + gap
        
        # Draw animals
        for item in render_data:
            animal_type = item["animal_type"]
            size = item["size"]
            color = item["color"]
            
            if state == "input":
                cx, cy = item["input_pos"]
            else:
                cx, cy = item["output_pos"]
            
            draw_animal(draw, animal_type, (int(cx), int(cy)), size, color)
        
        return canvas
    
    def get_task_type(self) -> str:
        """Get task type for prompt selection."""
        return self.sort_order


# ══════════════════════════════════════════════════════════════════════════════
#  TASK GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

class TaskGenerator(BaseGenerator):
    """
    Generator for animal size sorting task pairs.
    
    Generates image pairs showing:
    - Input: Scattered animals with different sizes
    - Output: Animals sorted by size and aligned at baseline
    """
    
    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.config: TaskConfig = config
        
        # Initialize video generator if enabled
        self.video_generator = None
        if getattr(config, 'generate_videos', False) and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(
                fps=getattr(config, 'video_fps', 10),
                output_format="mp4"
            )
    
    def _generate_task_data(self) -> dict[str, Any]:
        """Generate task-specific data for animal size sorting."""
        task = AnimalSizeSortingTask(
            width=self.config.image_size[0],
            height=self.config.image_size[1],
            num_animals=self.config.num_animals,
            min_size=self.config.min_size,
            max_size=self.config.max_size,
            sort_order=self.config.sort_order
        )
        
        return {
            "task": task,
            "task_type": task.get_task_type(),
            "num_animals": self.config.num_animals,
            "sort_order": self.config.sort_order
        }
    
    def _render_frame(self, task_data: dict[str, Any], state: str) -> Image.Image:
        """Render a frame for the given state."""
        task: AnimalSizeSortingTask = task_data["task"]
        return task.render(state)
    
    def generate_task_pair(self, task_id: str) -> TaskPair:
        """Generate one animal size sorting task pair."""
        
        # Generate task data
        task_data = self._generate_task_data()
        task: AnimalSizeSortingTask = task_data["task"]
        
        # Render input and output images
        first_image = self._render_frame(task_data, "input")
        final_image = self._render_frame(task_data, "output")
        
        # Generate video (optional)
        video_path = None
        if self.video_generator:
            video_path = self._generate_video(first_image, final_image, task_id, task)
        
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
    
    def _generate_video(
        self,
        first_image: Image.Image,
        final_image: Image.Image,
        task_id: str,
        task: AnimalSizeSortingTask
    ) -> Optional[str]:
        """Generate animation video showing animals sorting and aligning."""
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"
        
        # Create animation frames
        frames = self._create_animation_frames(task)
        
        result = self.video_generator.create_video_from_frames(frames, video_path)
        return str(result) if result else None
    
    def _create_animation_frames(
        self,
        task: AnimalSizeSortingTask,
        hold_frames: int = 5,
        transition_frames: int = 30
    ) -> list:
        """
        Create animation frames showing animals moving to sorted positions.
        """
        frames = []
        
        # Calculate output positions
        task.render("output")  # This populates output_pos
        
        # Get start and end positions
        start_positions = {i: item["input_pos"] for i, item in enumerate(task.data)}
        
        # Sort data to get correct output order
        sorted_indices = sorted(
            range(len(task.data)),
            key=lambda i: task.data[i]["size"],
            reverse=(task.sort_order == "descending")
        )
        
        # Recalculate output positions
        baseline_y = task.height - 80
        gap = 30
        sorted_data = [task.data[i] for i in sorted_indices]
        total_width = sum(item["size"] * 2.5 for item in sorted_data) + (len(sorted_data) - 1) * gap
        start_x = (task.width - total_width) // 2
        
        end_positions = {}
        current_x = start_x
        for new_idx, original_idx in enumerate(sorted_indices):
            size = task.data[original_idx]["size"]
            cx = current_x + size * 1.25
            cy = baseline_y - size * 1.2
            end_positions[original_idx] = (cx, cy)
            current_x += size * 2.5 + gap
        
        # Hold initial frame
        initial_frame = task.render("input")
        for _ in range(hold_frames):
            frames.append(initial_frame)
        
        # Transition frames
        for i in range(transition_frames):
            progress = i / (transition_frames - 1) if transition_frames > 1 else 1.0
            eased = self._ease_in_out(progress)
            
            frame = self._render_interpolated_frame(task, start_positions, end_positions, eased)
            frames.append(frame)
        
        # Hold final frame
        final_frame = task.render("output")
        for _ in range(hold_frames):
            frames.append(final_frame)
        
        return frames
    
    def _render_interpolated_frame(
        self,
        task: AnimalSizeSortingTask,
        start_positions: dict,
        end_positions: dict,
        progress: float
    ) -> Image.Image:
        """Render a frame with animals at interpolated positions."""
        canvas = Image.new("RGB", (task.width, task.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        # Draw baseline if progress > 0.5
        if progress > 0.5:
            baseline_y = task.height - 80
            draw.line([(30, baseline_y), (task.width - 30, baseline_y)], 
                     fill=(200, 200, 200), width=2)
        
        # Draw animals at interpolated positions
        for i, item in enumerate(task.data):
            animal_type = item["animal_type"]
            size = item["size"]
            color = item["color"]
            
            # Interpolate position
            sx, sy = start_positions[i]
            ex, ey = end_positions[i]
            
            cx = int(sx + (ex - sx) * progress)
            cy = int(sy + (ey - sy) * progress)
            
            draw_animal(draw, animal_type, (cx, cy), size, color)
        
        return canvas
    
    def _ease_in_out(self, t: float) -> float:
        """Ease-in-out function for smooth animation."""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
