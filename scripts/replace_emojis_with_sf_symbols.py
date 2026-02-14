#!/usr/bin/env python3
"""
Replace all emojis with SF Symbols across the project
Excludes node_modules, .git, and other irrelevant directories
"""

import os
import re
from pathlib import Path

# Emoji to SF Symbol mapping
EMOJI_MAPPINGS = {
    'basketball.fill': 'basketball.fill',
    'target': 'target',
    'chart.bar.fill': 'chart.bar.fill',
    'chart.line.uptrend.xyaxis': 'chart.line.uptrend.xyaxis',
    'chart.line.downtrend.xyaxis': 'chart.line.downtrend.xyaxis',
    'bolt.fill': 'bolt.fill',
    'flame.fill': 'flame.fill',
    'lightbulb.fill': 'lightbulb.fill',
    'paintpalette.fill': 'paintpalette.fill',
    'rocket.fill': 'rocket.fill',
    'iphone': 'iphone',
    'laptopcomputer': 'laptopcomputer',
    'magnifyingglass': 'magnifyingglass',
    'pencil': 'pencil',
    'checkmark.circle.fill': 'checkmark.circle.fill',
    'xmark.circle.fill': 'xmark.circle.fill',
    'star.fill': 'star.fill',
    'trophy.fill': 'trophy.fill',
    'gamecontroller.fill': 'gamecontroller.fill',
    'bell.fill': 'bell.fill',
    'envelope.fill': 'envelope.fill',
    'person.fill': 'person.fill',
    'person.2.fill': 'person.2.fill',
    'dollarsign.circle.fill': 'dollarsign.circle.fill',
    'calendar': 'calendar',
    'gearshape.fill': 'gearshape.fill',
    'lock.fill': 'lock.fill',
    'heart.fill': 'heart.fill',
    'powerplug.fill': 'powerplug.fill',
    'book.fill': 'book.fill',
    'checkmark': 'checkmark',
    'xmark': 'xmark',
    'hand.wave.fill': 'hand.wave.fill',
    'sparkles': 'sparkles',
    'figure.strengthtraining.traditional': 'figure.strengthtraining.traditional',
    'party.popper.fill': 'party.popper.fill',
    'alarm.fill': 'alarm.fill',
    'shippingbox.fill': 'shippingbox.fill',
    'wrench.and.screwdriver.fill': 'wrench.and.screwdriver.fill',
    'gift.fill': 'gift.fill',
    'figure.run': 'figure.run',
    'exclamationmark.triangle.fill': 'exclamationmark.triangle.fill',
    'burst.fill': 'burst.fill',
    'wrench.fill': 'wrench.fill',
    'film.fill': 'film.fill',
    'cloud.rainbow.fill': 'cloud.rainbow.fill',
    'tent.fill': 'tent.fill',
    'theatermasks.fill': 'theatermasks.fill',
    'medal.fill': 'medal.fill',
    'gearshape.fill': 'gearshape.fill',
    'wrench.and.screwdriver.fill': 'wrench.and.screwdriver.fill',
}

# File extensions to process
FILE_EXTENSIONS = {'.md', '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.yml', '.yaml', '.sh'}

# Directories to exclude
EXCLUDE_DIRS = {'node_modules', '.git', '.next', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv'}

def should_process_file(file_path: Path) -> bool:
    """Check if file should be processed"""
    # Check if any excluded directory is in the path
    for excluded in EXCLUDE_DIRS:
        if excluded in file_path.parts:
            return False

    # Check file extension
    return file_path.suffix in FILE_EXTENSIONS

def replace_emojis_in_file(file_path: Path) -> tuple[bool, int]:
    """Replace emojis in a single file. Returns (success, num_replacements)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        replacements = 0

        # Replace each emoji
        for emoji, sf_symbol in EMOJI_MAPPINGS.items():
            if emoji in content:
                count = content.count(emoji)
                content = content.replace(emoji, sf_symbol)
                replacements += count

        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, replacements

        return False, 0

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0

def process_directory(root_dir: Path):
    """Process all files in directory"""
    files_changed = []
    total_replacements = 0

    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and should_process_file(file_path):
            changed, replacements = replace_emojis_in_file(file_path)
            if changed:
                files_changed.append(file_path)
                total_replacements += replacements
                print(f"checkmark {file_path.relative_to(root_dir)} ({replacements} replacements)")

    return files_changed, total_replacements

if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    print(f"Processing files in: {project_root}")
    print(f"Excluding: {', '.join(EXCLUDE_DIRS)}")
    print("-" * 80)

    files_changed, total_replacements = process_directory(project_root)

    print("-" * 80)
    print(f"\nSummary:")
    print(f"Files changed: {len(files_changed)}")
    print(f"Total replacements: {total_replacements}")

    if files_changed:
        print("\nChanged files:")
        for file_path in files_changed:
            print(f"  - {file_path.relative_to(project_root)}")
