from textnode import *
import re

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    full_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if not stripped_block:
            continue
        full_blocks.append(stripped_block)

    return full_blocks