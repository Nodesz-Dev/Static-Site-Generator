import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from block_markdown import *


class TestMarkdownMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_empty_string(self):
        text = ""
        blocks = markdown_to_blocks(text)
        expected = []
        self.assertEqual(expected, blocks)

    def test_markdown_to_blocks_single_paragraph(self):
        text = "This is **bolded** paragraph"
        blocks = markdown_to_blocks(text)
        expected = ["This is **bolded** paragraph"]
        self.assertEqual(expected, blocks)

    def test_markdown_to_blocks_multiple_paragraphs(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks_trailing_whitepace(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items                                                                
                                                  
"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks_whitespace_in_paragraph(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same           paragraph on a new line                                          
"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same           paragraph on a new line",
            ]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks_empty_blocks(self):
        text = """
This is **bolded** paragraph






This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
            ]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks_singe_newlines(self):
        text = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line                                          
"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks_large_input(self):
        text = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    

This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 

This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 

This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 

This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 
"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ]
        self.assertEqual(expected,blocks)

    def test_markdown_to_blocks_special_characters(self):
        text = """
This is **bolded** paragraph

This is* another paragraph* with _italic_ text and `code` here
This is the same paragraph - on a new line?

- This is a list
- with items
"""
        blocks = markdown_to_blocks(text)
        expected = [
                "This is **bolded** paragraph",
                "This is* another paragraph* with _italic_ text and `code` here\nThis is the same paragraph - on a new line?",
                "- This is a list\n- with items",
            ]
        self.assertEqual(expected,blocks)

    
if __name__ == "__main__":
    unittest.main()