from textnode import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    full_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if not stripped_block:
            continue
        full_blocks.append(stripped_block)

    return full_blocks

def block_to_block_type(block):
    split_lines = block.split("\n")
    
    if block.startswith(("#","##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if len(split_lines) > 0 and split_lines[0].startswith("```") and split_lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in split_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in split_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    i = 1
    if block.startswith(f"{i}. "):
        for line in split_lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    