import re
from typing import Tuple, Dict, Any


def extract_frontmatter(raw_content: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract standard YAML frontmatter bounded by --- and content.
    Converts 'tags' value into a Python list.
    """
    frontmatter_pattern = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
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

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # Strip trailing/leading quotes
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]

        if key == 'tags':
            # Handle array format [tag1, tag2] or comma separated string
            if value.startswith('[') and value.endswith(']'):
                tags_str = value[1:-1]
                metadata[key] = [t.strip().strip("'").strip('"')
                                 for t in tags_str.split(',') if t.strip()]
            else:
                metadata[key] = [t.strip()
                                 for t in value.split(',') if t.strip()]
        else:
            metadata[key] = value

    return metadata, content
