# Path Planning Task Generator

A visual reasoning task generator that creates image pairs showing pathfinding through obstacle grids.

## Task Description

The path planning task involves:
- **Input**: A grid map with randomly placed obstacles (black), a start point (red circle), and a goal point (green circle)
- **Output**: The same map with the shortest path drawn from start to goal, avoiding all obstacles

The algorithm uses Breadth-First Search (BFS) to find the optimal path.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from src import TaskConfig, TaskGenerator
from core.output_writer import OutputWriter

# Create configuration
config = TaskConfig(
    output_dir="./output",
    num_samples=10,
    grid_width=15,
    grid_height=10,
    obstacle_density=0.25
)

# Generate tasks
generator = TaskGenerator(config)
writer = OutputWriter(config)

for i in range(config.num_samples):
    task_id = f"path_planning_{i:04d}"
    task_pair = generator.generate_task_pair(task_id)
    writer.write(task_pair)
```

### Command Line

```bash
# Generate 10 task pairs
python examples/generate.py --output ./output --num-tasks 10

# Generate with larger grid
python examples/generate.py --output ./output --grid-width 20 --grid-height 15

# Generate with more obstacles and videos
python examples/generate.py --output ./output --obstacle-density 0.3 --generate-videos
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `grid_width` | 15 | Number of columns in the grid (5-30) |
| `grid_height` | 10 | Number of rows in the grid (5-20) |
| `cell_size` | 40 | Size of each cell in pixels (20-80) |
| `obstacle_density` | 0.25 | Percentage of cells that are obstacles (0.1-0.5) |
| `generate_videos` | False | Whether to generate ground truth videos |

## Output Structure

```
output/
├── images/
│   ├── path_planning_0000_input.png
│   ├── path_planning_0000_output.png
│   └── ...
├── videos/  (if enabled)
│   ├── path_planning_0000_ground_truth.mp4
│   └── ...
└── metadata.json
```

## Project Structure

```
path_planning/
├── core/               # Core utilities (copied from main project)
│   ├── base_generator.py
│   ├── schemas.py
│   ├── image_utils.py
│   ├── video_utils.py
│   └── output_writer.py
├── src/                # Task-specific implementation
│   ├── generator.py    # TaskGenerator class with BFS pathfinding
│   ├── config.py       # TaskConfig class
│   └── prompts.py      # Task prompts
├── examples/
│   └── generate.py     # CLI entry point
├── requirements.txt
└── README.md
```

## Algorithm Details

The path planning task uses **Breadth-First Search (BFS)** to find the shortest path:
1. Generate a random grid with obstacles
2. Place start and goal points on empty cells
3. Use BFS to explore the grid level by level
4. Reconstruct the path from goal back to start
5. If no path exists, regenerate the map until solvable

## License

MIT License
