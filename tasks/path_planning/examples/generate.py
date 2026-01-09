#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       PATH PLANNING TASK - EXAMPLE SCRIPT                     ║
║                                                                               ║
║  Generate path planning task image pairs                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python generate.py --output ./output --num-tasks 10
    python generate.py --output ./output --grid-width 20 --grid-height 15
    python generate.py --output ./output --obstacle-density 0.3 --generate-videos
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import TaskConfig, TaskGenerator
from core.output_writer import OutputWriter


def main():
    parser = argparse.ArgumentParser(
        description="Generate path planning task image pairs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate 10 task pairs
    python generate.py --output ./output --num-tasks 10
    
    # Generate with larger grid
    python generate.py --output ./output --grid-width 20 --grid-height 15
    
    # Generate with more obstacles and videos
    python generate.py --output ./output --obstacle-density 0.3 --generate-videos
        """
    )
    
    # Output settings
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./output",
        help="Output directory for generated data"
    )
    parser.add_argument(
        "--num-tasks", "-n",
        type=int,
        default=5,
        help="Number of task pairs to generate"
    )
    
    # Grid settings
    parser.add_argument(
        "--grid-width",
        type=int,
        default=15,
        help="Number of columns in the grid (5-30)"
    )
    parser.add_argument(
        "--grid-height",
        type=int,
        default=10,
        help="Number of rows in the grid (5-20)"
    )
    parser.add_argument(
        "--cell-size",
        type=int,
        default=40,
        help="Size of each cell in pixels (20-80)"
    )
    parser.add_argument(
        "--obstacle-density",
        type=float,
        default=0.25,
        help="Percentage of cells that are obstacles (0.1-0.5)"
    )
    
    # Video settings
    parser.add_argument(
        "--generate-videos",
        action="store_true",
        help="Generate ground truth videos"
    )
    parser.add_argument(
        "--video-fps",
        type=int,
        default=10,
        help="Video frames per second"
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = TaskConfig(
        output_dir=args.output,
        num_samples=args.num_tasks,
        grid_width=args.grid_width,
        grid_height=args.grid_height,
        cell_size=args.cell_size,
        obstacle_density=args.obstacle_density,
        generate_videos=args.generate_videos,
        video_fps=args.video_fps,
    )
    
    # Calculate image size
    img_width = args.grid_width * args.cell_size
    img_height = args.grid_height * args.cell_size
    
    print(f"╔{'═' * 60}╗")
    print(f"║{'PATH PLANNING TASK GENERATOR':^60}║")
    print(f"╚{'═' * 60}╝")
    print()
    print(f"  Output directory:   {args.output}")
    print(f"  Number of tasks:    {args.num_tasks}")
    print(f"  Grid size:          {args.grid_width}x{args.grid_height}")
    print(f"  Cell size:          {args.cell_size}px")
    print(f"  Image size:         {img_width}x{img_height}")
    print(f"  Obstacle density:   {args.obstacle_density:.0%}")
    print(f"  Generate videos:    {args.generate_videos}")
    print()
    
    # Create generator and output writer
    generator = TaskGenerator(config)
    writer = OutputWriter(config)
    
    # Generate task pairs
    print("Generating task pairs...")
    for i in range(args.num_tasks):
        task_id = f"path_planning_{i:04d}"
        task_pair = generator.generate_task_pair(task_id)
        writer.write(task_pair)
        print(f"  [{i+1}/{args.num_tasks}] Generated {task_id}")
    
    print()
    print(f"✓ Generation complete! Output saved to: {args.output}")


if __name__ == "__main__":
    main()
