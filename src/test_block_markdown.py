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

class TestMarkdownBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph block"
        block_type = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(expected, block_type)

    def test_block_to_block_type_heading(self):
        blocks = ["#This is a heading block",
                  "##This is a heading block",
                  "###This is a heading block",
                  "####This is a heading block",
                  "#####This is a heading block",
                  "######This is a heading block"
                  ]
        block_type0 = block_to_block_type(blocks[0])
        block_type1 = block_to_block_type(blocks[1])
        block_type2 = block_to_block_type(blocks[2])
        block_type3 = block_to_block_type(blocks[3])
        block_type4 = block_to_block_type(blocks[4])
        block_type5 = block_to_block_type(blocks[5])
        expected = BlockType.HEADING
        self.assertEqual(expected, block_type0)
        self.assertEqual(expected, block_type1)
        self.assertEqual(expected, block_type2)
        self.assertEqual(expected, block_type3)
        self.assertEqual(expected, block_type4)
        self.assertEqual(expected, block_type5)

    def test_block_to_block_type_invalid_heading(self):
        blocks = ["This is a heading block#",
                  "This is a heading block\n## This is a heading block",
                  ">###This is a heading block",
                  "-####This is a heading block",
                  "1#####This is a heading block",
                  "This### is a heading block"
                  ]
        block_type0 = block_to_block_type(blocks[0])
        block_type1 = block_to_block_type(blocks[1])
        block_type2 = block_to_block_type(blocks[2])
        block_type3 = block_to_block_type(blocks[3])
        block_type4 = block_to_block_type(blocks[4])
        block_type5 = block_to_block_type(blocks[5])
        expected = BlockType.HEADING
        self.assertNotEqual(expected, block_type0)
        self.assertNotEqual(expected, block_type1)
        self.assertNotEqual(expected, block_type2)
        self.assertNotEqual(expected, block_type3)
        self.assertNotEqual(expected, block_type4)
        self.assertNotEqual(expected, block_type5)

    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        block_type = block_to_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(expected, block_type)

    def test_block_to_block_type_invalid_code(self):
        blocks = ["``This is a code block```",
                  "`This is a code block```",
                  "This is a code block```",
                  "```This is a code block``",
                  "```This is a code block`",
                  "```This is a code block"
                  ]
        block_type0 = block_to_block_type(blocks[0])
        block_type1 = block_to_block_type(blocks[1])
        block_type2 = block_to_block_type(blocks[2])
        block_type3 = block_to_block_type(blocks[3])
        block_type4 = block_to_block_type(blocks[4])
        block_type5 = block_to_block_type(blocks[5])
        expected = BlockType.CODE
        self.assertNotEqual(expected, block_type0)
        self.assertNotEqual(expected, block_type1)
        self.assertNotEqual(expected, block_type2)
        self.assertNotEqual(expected, block_type3)
        self.assertNotEqual(expected, block_type4)
        self.assertNotEqual(expected, block_type5)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote block"
        block_type = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(expected, block_type)

    def test_block_to_block_type_invalid_quote(self):
        block = "->This is a quote block"
        block_type = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertNotEqual(expected, block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a ordered list block\n2. This is an ordered list block\n3. This is an ordered list block\n4. This is an ordered list block"
        block_type = block_to_block_type(block)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(expected, block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a ordered list block\n2. This is an ordered list block\n2. This is an ordered list block\n4. This is an ordered list block"
        block_type = block_to_block_type(block)
        expected = BlockType.ORDERED_LIST
        self.assertNotEqual(expected, block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a unordered lsit block\n- This is a unordered lsit block\n>- This is a unordered lsit block\n- This is a unordered lsit block\n"
        block_type = block_to_block_type(block)
        expected = BlockType.UNORDERED_LIST
        self.assertNotEqual(expected, block_type)
    
if __name__ == "__main__":
    unittest.main()