import textwrap
from typing import List


def markdown_to_lines(text: str, max_cols: int) -> List[str]:
    """Very small subset of markdown: wrap lines to max_cols."""
    lines: List[str] = []
    for raw in text.splitlines():
        wrapped = textwrap.wrap(raw, width=max_cols) or ['']
        lines.extend(wrapped)
    return lines
