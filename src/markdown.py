from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.texttype == TextType.TEXT:
            split_nodes = []
            sections = node.text.split(delimiter)
            for i in range(len(sections)):
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.TEXT))
                elif i % 2 > 0:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)


    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(regex, text)
    return result

def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)

