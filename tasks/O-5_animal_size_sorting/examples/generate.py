#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   ANIMAL SIZE SORTING TASK - EXAMPLE SCRIPT                   ║
║                                                                               ║
║  Generate animal size sorting task image pairs                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python generate.py --output ./output --num-tasks 10
    python generate.py --output ./output --num-animals 6 --sort-order descending
    python generate.py --output ./output --generate-videos
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
        description="Generate animal size sorting task image pairs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate 10 task pairs
    python generate.py --output ./output --num-tasks 10
    
    # Generate with 6 animals in descending order
    python generate.py --output ./output --num-animals 6 --sort-order descending
    
    # Generate with ground truth videos
    python generate.py --output ./output --generate-videos
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
    
    # Task settings
    parser.add_argument(
        "--num-animals",
        type=int,
        default=5,
        help="Number of animals to sort (3-6)"
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=30,
        help="Minimum animal size in pixels"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=80,
        help="Maximum animal size in pixels"
    )
    parser.add_argument(
        "--sort-order",
        type=str,
        choices=["ascending", "descending"],
        default="ascending",
        help="Sort order: ascending or descending"
    )
    
    # Image settings
    parser.add_argument(
        "--width",
        type=int,
        default=800,
        help="Image width in pixels"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=500,
        help="Image height in pixels"
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
        image_size=(args.width, args.height),
        num_animals=args.num_animals,
        min_size=args.min_size,
        max_size=args.max_size,
        sort_order=args.sort_order,
        generate_videos=args.generate_videos,
        video_fps=args.video_fps,
    )
    
    print(f"╔{'═' * 60}╗")
    print(f"║{'ANIMAL SIZE SORTING TASK GENERATOR':^60}║")
    print(f"╚{'═' * 60}╝")
    print()
    print(f"  Output directory: {args.output}")
    print(f"  Number of tasks:  {args.num_tasks}")
    print(f"  Number of animals:{args.num_animals}")
    print(f"  Size range:       {args.min_size}-{args.max_size}px")
    print(f"  Sort order:       {args.sort_order}")
    print(f"  Image size:       {args.width}x{args.height}")
    print(f"  Generate videos:  {args.generate_videos}")
    print()
    
    # Create generator and output writer
    generator = TaskGenerator(config)
    writer = OutputWriter(args.output)
    
    # Generate task pairs
    print("Generating task pairs...")
    for i in range(args.num_tasks):
        task_id = f"O-5_animal_size_sorting_{i:04d}"
        task_pair = generator.generate_task_pair(task_id)
        writer.write_task_pair(task_pair)
        print(f"  [{i+1}/{args.num_tasks}] Generated {task_id}")
    
    print()
    print(f"✓ Generation complete! Output saved to: {args.output}")


if __name__ == "__main__":
    main()
