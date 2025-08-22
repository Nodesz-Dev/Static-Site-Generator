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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.texttype != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        sections = []
        for image in images:
            text_to_split = sections.pop() if sections else node.text
            sections.extend(text_to_split.split(f"![{image[0]}]({image[1]})",1))

        for i in range(len(sections)-1):
            if sections[i]:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            if len(images) > 0 and i < len(images):
                new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
        if sections and sections[-1]:
            new_nodes.append(TextNode(sections[-1], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.texttype != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        sections = []
        for link in links:
            text_to_split = sections.pop() if sections else node.text
            sections.extend(text_to_split.split(f"[{link[0]}]({link[1]})",1))

        for i in range(len(sections)-1):
            if sections[i]:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            if len(links) > 0 and i < len(links):
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
        if sections and sections[-1]:
            new_nodes.append(TextNode(sections[-1], TextType.TEXT))

    return new_nodes