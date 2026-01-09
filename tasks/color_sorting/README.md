# Color Sorting Task Data Generator 🎨

A data generator for creating synthetic "Color Sorting" reasoning tasks. Objects (colored blocks) must be sorted into containers that match their colors.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install -e .

# 2. Generate tasks
python examples/generate.py --num-samples 50
```

---

## 📁 Structure

```
color_sorting/
├── core/                    # Standard utilities
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # Color sorting task logic
│   ├── generator.py        # Task generator
│   ├── prompts.py          # Prompt templates
│   └── config.py           # Task configuration
├── examples/
│   └── generate.py         # Entry point
└── data/questions/         # Generated output
```

---

## 🎯 Task Description

**Task Name**: Color-based Bin Sorting (基于颜色的归类分拣)

**Visual Logic**:
- **Input**: Canvas with colored containers (empty frames) and scattered colored blocks
- **Output**: All blocks moved into their matching color containers, arranged in a grid layout

**Prompt**: "The image shows scattered colored blocks and empty containers. Move each block into the container that matches its color. Arrange the blocks neatly inside the containers."

---

## ⚙️ Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_colors` | 2 | Number of color categories (2-6) |
| `items_per_color` | 4 | Number of blocks per color |
| `block_size` | 25 | Size of each block in pixels |
| `image_size` | (600, 400) | Canvas dimensions |
| `video_fps` | 10 | Video frame rate |

---

## 📦 Output Format

```
data/questions/color_sorting_task/{task_id}/
├── first_frame.png    # Scattered blocks + empty containers
├── final_frame.png    # Sorted blocks in matching containers
├── prompt.txt         # Task instructions
└── ground_truth.mp4   # Animation of sorting process
```
