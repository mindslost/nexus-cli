import re
from typing import Tuple, Dict, Any


def extract_frontmatter(raw_content: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract standard YAML frontmatter bounded by --- and content.
    Converts 'tags' value into a Python list.
    """
    # Robustly identify the frontmatter block
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

        # Split only on the first colon to allow colons in values
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # Handle quoted values
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
            # Simple unescape for double quotes if the value was double quoted
            if line.strip().split(':', 1)[1].strip().startswith('"'):
                value = value.replace('\\"', '"')

        if key == 'tags':
            # Handle YAML-style array: [tag1, tag2]
            if value.startswith('[') and value.endswith(']'):
                tags_str = value[1:-1]
                # Split by comma and strip quotes and whitespace
                metadata[key] = [
                    t.strip().strip("'").strip('"')
                    for t in tags_str.split(',') if t.strip()
                ]
            else:
                # Handle comma-separated string
                metadata[key] = [
                    t.strip()
                    for t in value.split(',') if t.strip()
                ]
        else:
            metadata[key] = value

    return metadata, content
