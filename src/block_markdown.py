from textnode import *
import re

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    full_blocks = []
    for block in split_blocks:
        if block == "":
            continue
        stripped_block = block.strip()
        full_blocks.append(stripped_block)

    return full_blocks