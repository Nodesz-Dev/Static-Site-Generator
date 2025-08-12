from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
        TEXT = "text"
        BOLD = "bold"
        ITALIC = "italic"
        CODE = "code"
        LINK = "link"
        IMAGE = "image"

class TextNode:
        
        def __init__(self, text, texttype, url=None):
            self.text = text
            self.texttype = texttype
            self.url = url

        def __eq__(self, target):
            return (self.text == target.text and 
                    self.texttype == target.texttype and 
                    self.url == target.url)
        
        def __repr__(self):
              return f"TextNode({self.text}, {self.texttype.value}, {self.url})"
        
def text_node_to_html_node(text_node):
        match text_node.texttype:
                case TextType.TEXT:
                      return LeafNode(None, text_node.text)
                case TextType.BOLD:
                      return LeafNode("b", text_node.text)
                case TextType.ITALIC:
                        return LeafNode("i", text_node.text)
                case TextType.CODE:
                      return LeafNode("code", text_node.text)
                case TextType.LINK:
                      return LeafNode("a", text_node.text, {"href": text_node.url})
                case TextType.IMAGE:
                      return LeafNode("img", None,{"src": text_node.url, "alt": text_node.text})
                case _:
                    raise ValueError(f"Error: TextType mismatch: {text_node.texttype}")