# O-2 Size Sorting Task Generator

A visual reasoning task generator that creates image pairs showing bars being sorted by height.

## Task Description

The size sorting task involves:
- **Input**: Scattered rectangular bars of different heights and colors positioned randomly on a canvas
- **Output**: The same bars sorted by height (ascending or descending) and aligned at a baseline

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
    num_bars=7,
    sort_order="ascending"
)

# Generate tasks
generator = TaskGenerator(config)
writer = OutputWriter(config)

for i in range(config.num_samples):
    task_id = f"size_sorting_{i:04d}"
    task_pair = generator.generate_task_pair(task_id)
    writer.write(task_pair)
```

### Command Line

```bash
# Generate 10 task pairs
python examples/generate.py --output ./output --num-tasks 10

# Generate with 10 bars in descending order
python examples/generate.py --output ./output --num-bars 10 --sort-order descending

# Generate with ground truth videos
python examples/generate.py --output ./output --generate-videos
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_bars` | 7 | Number of bars to sort (3-15) |
| `bar_width` | 40 | Width of each bar in pixels |
| `min_height` | 50 | Minimum bar height in pixels |
| `max_height` | 250 | Maximum bar height in pixels |
| `sort_order` | "ascending" | Sort order: "ascending" or "descending" |
| `image_size` | (800, 400) | Output image dimensions |
| `generate_videos` | False | Whether to generate ground truth videos |

## Output Structure

```
output/
├── images/
│   ├── O-2_size_sorting_0000_input.png
│   ├── O-2_size_sorting_0000_output.png
│   └── ...
├── videos/  (if enabled)
│   ├── O-2_size_sorting_0000_ground_truth.mp4
│   └── ...
└── metadata.json
```

## Project Structure

```
O-2_size_sorting/
├── core/               # Core utilities (copied from main project)
│   ├── base_generator.py
│   ├── schemas.py
│   ├── image_utils.py
│   ├── video_utils.py
│   └── output_writer.py
├── src/                # Task-specific implementation
│   ├── generator.py    # TaskGenerator class
│   ├── config.py       # TaskConfig class
│   └── prompts.py      # Task prompts
├── examples/
│   └── generate.py     # CLI entry point
├── requirements.txt
└── README.md
```

## License

MIT License
