# O-5 Animal Size Sorting Task Generator 🐾

A visual reasoning task generator that combines animal faces with size sorting.

## Task Description

The animal size sorting task involves:
- **Input**: Scattered animal faces (cat, dog, rabbit, bear, panda, fox) of different sizes positioned randomly on a canvas
- **Output**: The same animals sorted by size (ascending or descending) and aligned at a baseline

This task combines visual object recognition (different animal faces) with spatial reasoning (size comparison and sorting).

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
    num_animals=5,
    sort_order="ascending"
)

# Generate tasks
generator = TaskGenerator(config)
writer = OutputWriter(config)

for i in range(config.num_samples):
    task_id = f"O-5_animal_size_sorting_{i:04d}"
    task_pair = generator.generate_task_pair(task_id)
    writer.write(task_pair)
```

### Command Line

```bash
# Generate 10 task pairs
python examples/generate.py --output ./output --num-tasks 10

# Generate with 6 animals in descending order
python examples/generate.py --output ./output --num-animals 6 --sort-order descending

# Generate with ground truth videos
python examples/generate.py --output ./output --generate-videos
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_animals` | 5 | Number of animals to sort (3-6) |
| `min_size` | 30 | Minimum animal size in pixels |
| `max_size` | 80 | Maximum animal size in pixels |
| `sort_order` | "ascending" | Sort order: "ascending" or "descending" |
| `image_size` | (800, 500) | Output image dimensions |
| `generate_videos` | False | Whether to generate ground truth videos |

## Animal Types

The generator includes 6 different animal faces:
- 🐱 **Cat** - Orange cat with pointy ears and whiskers
- 🐶 **Dog** - Brown dog with floppy ears and tongue
- 🐰 **Rabbit** - Pink rabbit with long ears and buck teeth
- 🐻 **Bear** - Brown bear with round ears and smile
- 🐼 **Panda** - Black and white panda with eye patches
- 🦊 **Fox** - Orange fox with pointy ears and white muzzle

## Output Structure

```
output/
├── images/
│   ├── O-5_animal_size_sorting_0000_input.png
│   ├── O-5_animal_size_sorting_0000_output.png
│   └── ...
├── videos/  (if enabled)
│   ├── O-5_animal_size_sorting_0000_ground_truth.mp4
│   └── ...
└── metadata.json
```

## Project Structure

```
O-5_animal_size_sorting/
├── core/               # Core utilities (copied from main project)
│   ├── base_generator.py
│   ├── schemas.py
│   ├── image_utils.py
│   ├── video_utils.py
│   └── output_writer.py
├── src/                # Task-specific implementation
│   ├── generator.py    # TaskGenerator class with animal drawing
│   ├── config.py       # TaskConfig class
│   └── prompts.py      # Task prompts
├── examples/
│   └── generate.py     # CLI entry point
├── requirements.txt
└── README.md
```

## License

MIT License
