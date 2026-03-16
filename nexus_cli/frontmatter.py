"""
Frontmatter parsing for the Nexus CLI.

This module provides utilities to extract YAML-like frontmatter from
Markdown files. It handles quoted values, escaped characters, and
supports both comma-separated and YAML-array styles for tags.
"""

import re
from typing import Tuple, Dict, Any


def extract_frontmatter(raw_content: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract standard YAML frontmatter bounded by '---' from the start of a string.

    Args:
        raw_content: The full content of a Markdown file, including frontmatter.

    Returns:
        A tuple of (metadata_dict, body_content).
        - metadata_dict: Dictionary of parsed keys and values.
        - body_content: The rest of the file after the frontmatter block.
        If no frontmatter is found, returns ({}, raw_content).
    """
    # Robustly identify the frontmatter block using a non-greedy DOTALL regex.
    # It looks for '---' at the very beginning of the string and another '---'
    # on its own line.
    frontmatter_pattern = re.compile(
        r"^---\s*\n(.*?)\n---\s*(?:\n|$)(.*)$", re.DOTALL)
    match = frontmatter_pattern.match(raw_content.lstrip())

    if not match:
        return {}, raw_content

    yaml_str = match.group(1)
    content = match.group(2)

    metadata: Dict[str, Any] = {}

    for line in yaml_str.strip().split('\n'):
        line = line.strip()
        if not line or ':' not in line:
            continue

        # Split only on the first colon to allow colons in values (e.g., titles)
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # Handle quoted values (both single and double quotes)
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            # Remove the surrounding quotes
            value = value[1:-1]

            # Simple unescape for double quotes if the value was double quoted
            # This handles common cases like 'title: "A \"Special\" Note"'
            if line.strip().split(':', 1)[1].strip().startswith('"'):
                value = value.replace('\\"', '"')

        if key == 'tags':
            # Handle YAML-style array: [tag1, tag2]
            if value.startswith('[') and value.endswith(']'):
                tags_str = value[1:-1]
                # Split by comma and strip quotes/whitespace from each tag
                metadata[key] = [
                    t.strip().strip("'").strip('"')
                    for t in tags_str.split(',') if t.strip()
                ]
            else:
                # Handle comma-separated string: tag1, tag2
                metadata[key] = [
                    t.strip()
                    for t in value.split(',') if t.strip()
                ]
        else:
            metadata[key] = value

    return metadata, content
