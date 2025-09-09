from textnode import *
from htmlnode import *
from inline_markdown import text_to_textnodes
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
        block = block.strip()
        if not block:
            continue
        full_blocks.append(block)

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
    if block.startswith(f"1. "):
        i = 1
        for line in split_lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    markdown_block = markdown_to_blocks(markdown)
    children = []

    for block in markdown_block:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError("Blocktype Error: Invalid block type")


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    hash_amount = 0
    for char in block:
        if char == "#":
            hash_amount += 1
        else:
            break

    if hash_amount + 1 >= len(block):
        raise ValueError(f"Invalid heading count: {hash_amount}")
    text = block[hash_amount + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{hash_amount}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ol", html_nodes)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ul", html_nodes)

def text_to_children(text):
    inline_markdown = text_to_textnodes(text)
    children = []
    for textnode in inline_markdown:
        html_node = text_node_to_html_node(textnode)
        children.append(html_node)

    return children