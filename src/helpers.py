from typing import Tuple, List
import re

from  delimiter import text_to_textnodes
from htmlnode import text_node_to_html_node  # or wherever it's defined

def text_to_children(text: str):
    tnodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in tnodes]

def clean_quote_block(block: str) -> str:
    lines = block.splitlines()
    cleaned = []
    for line in lines:
        if line.startswith("> "):
            cleaned.append(line[2:])
        elif line.startswith(">"):
            cleaned.append(line[1:])
        else:
            cleaned.append(line)
    return "\n".join(cleaned)
def parse_heading_block(block: str) -> Tuple[int, str]:
    line = block.splitlines()[0] if block else ""
    if not line.startswith("#"):
        raise Exception(f"invalid block: {line}")
    level = 0
    for ch in line:
        if ch == "#":
            level += 1
        else:
            break
    if level > 6:
        raise Exception(f"invalid block: {line}")

    text = line[level:]
    if text.startswith(" "):
        text = text[1:]

    if len(text) == 0:
        raise Exception(f"invalid block: {line}")
    return level, text


def parse_code_block(block:str) -> str :
    lines = block.splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        lines = lines[1:-1]
    return "\n".join(lines)


def parse_list_items(block:str, ordered=False) -> List[str]:
    items = []
    for raw in block.splitlines():
        line = raw.lstrip()
        if not line:
            continue
        if ordered:
            m = re.match(r"(\d+)\.\s+(.*)", line)
            if m:
                items.append(m.group(2))
        else:
            if line.startswith("- ") or line.startswith("* "):
                items.append(line[2:])
    return items

def paragraph_text(block: str) -> str:
    lines = [line.strip() for line in block.splitlines()]
    # join with single spaces so it renders as one paragraph
    return " ".join([l for l in lines if l != ""])