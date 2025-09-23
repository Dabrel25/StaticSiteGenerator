from enum import Enum
import re
from typing import List
from helpers import *
from

from src.htmlnode import HTMLNode


class BlockType(Enum):
    """Enumeration of supported markdown block types."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def block_to_block_type(block: str) -> BlockType:
    """Classify a markdown block into a BlockType.

    The function assumes `block` has already been trimmed and contains no
    leading/trailing blank lines. Detection order follows common markdown
    precedence: heading, fenced code, quote, ordered list, unordered list,
    otherwise paragraph.
    """
    lines = block.splitlines() or [""]

    # Heading: one to six leading '# ' on the first line
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Fenced code block delimited by triple backticks on first and last lines
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote: all lines start with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Ordered list: lines start with incrementing 'N. '
    expected = 1
    for line in lines:
        m = re.match(r"^(\d+)\. ", line)
        if not m or int(m.group(1)) != expected:
            break
        expected += 1
    else:
        return BlockType.ORDERED_LIST

    # Unordered list: all lines start with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> List[str]:
    """Split raw markdown text into trimmed blocks separated by blank lines."""
    blocks = markdown.split("\n\n")
    filtered_blocks: List[str] = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def markdown_to_html_nodes(markdown: str):
    """Convert markdown to a tree of HTML nodes."""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        bt = block_to_block_type(block)

        if bt == BlockType.HEADING:
            level, text = parse_heading_block(block)
            kids = text_to_children(text)
            children.append(HTMLNode(tag=f"h{level}", children=kids))

        elif bt == BlockType.PARAGRAPH:
            text = paragraph_text(block)
            kids = text_to_children(text)
            children.append(HTMLNode(tag="p", children=kids))

        elif bt == BlockType.QUOTE:
            text = paragraph_text(block)
            kids = text_to_children(text)
            children.append(HTMLNode(tag="blockquote", children=kids))

        elif bt == BlockType.CODE:
            code_text = parse_code_block(block)
            code_node = HTMLNode(tag="code", value=code_text)
            children.append(HTMLNode(tag="pre", children=[code_node]))

        elif bt == BlockType.ORDERED_LIST:
            items = parse_list_items(block, ordered=True)
            li_nodes = [HTMLNode(tag="li",children=text_to_children(it))for it in items]
            children.append(HTMLNode(tag="ol", children=li_nodes))

        elif bt == BlockType.UNORDERED_LIST:
            items = parse_list_items(block, ordered=False)
            li_nodes = [HTMLNode(tag="li",children=text_to_children(it))for it in items]
            children.append(HTMLNode(tag="ul", children=li_nodes))

        else:
            # fallback: treat as paragraph
            text = paragraph_text(block)
            kids = text_to_children(text)
            children.append(HTMLNode(tag="p", children=kids))

    return HTMLNode(tag="div", children=children)
