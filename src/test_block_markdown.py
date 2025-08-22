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

    def test_block_to_block_type_quote_multiple_lines(self):
        block0 = ">This is a quote block\n>This is a quote block\n>This is a quote block"
        block1 = ">This is a quote block\nThis is a quote block\n>This is a quote block"
        block_type0 = block_to_block_type(block0)
        block_type1 = block_to_block_type(block1)
        expected = BlockType.QUOTE
        self.assertEqual(expected, block_type0)
        self.assertNotEqual(expected, block_type1)

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

    def test_block_to_block_type_invalid_ordered_list(self):
        block = "1. This is a ordered list block\n2. This is an ordered list block\n2. This is an ordered list block\n4. This is an ordered list block"
        block_type = block_to_block_type(block)
        expected = BlockType.ORDERED_LIST
        self.assertNotEqual(expected, block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a unordered lsit block\n- This is a unordered lsit block\n- This is a unordered lsit block\n- This is a unordered lsit block"
        block_type = block_to_block_type(block)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(expected, block_type)

    def test_block_to_block_type_invalid_unordered_list(self):
        block = "- This is a unordered lsit block\n>- This is a unordered lsit block\n- This is a unordered lsit block\n- This is a unordered lsit block"
        block_type = block_to_block_type(block)
        expected = BlockType.UNORDERED_LIST
        self.assertNotEqual(expected, block_type)

    def test_block_to_block_type_inline_markdown(self):
        block = "This is a _paragraph_ block"
        block_type = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(expected, block_type)

    def test_block_to_block_empty(self):
        block = ""
        block_type = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(expected, block_type)

class TestParagraphToHtmlNode(unittest.TestCase):
    def test_paragraph_to_html_node(self):
        block = "This is a paragraph"
        html_node = paragraph_to_html_node(block)
        self.assertEqual(html_node.tag, "p")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    

class TestHeadingToHtmlNode(unittest.TestCase):
    def test_heading_to_html_node(self):
        block = "# Heading"
        html_node = heading_to_html_node(block)
        self.assertEqual(html_node.tag, "h1")

    def test_invalid_heading_count(self):
        block = "#"
        with self.assertRaises(ValueError):
            heading_to_html_node(block)

class TestCodeToHtmlNode(unittest.TestCase):
    def test_code_to_html_node(self):
        block = "```\ncode\n```"
        html_node = code_to_html_node(block)
        self.assertEqual(html_node.tag, "pre")

    def test_invalid_code_block(self):
        block = "```\ncode"
        with self.assertRaises(ValueError):
            code_to_html_node(block)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

class TestQuoteToHtmlNode(unittest.TestCase):
    def test_quote_to_html_node(self):
        block = "> quote"
        html_node = quote_to_html_node(block)
        self.assertEqual(html_node.tag, "blockquote")

    def test_invalid_quote_block(self):
        block = "quote"
        with self.assertRaises(ValueError):
            quote_to_html_node(block)

class TestOrderedListToHtmlNode(unittest.TestCase):
    def test_ordered_list_to_html_node(self):
        block = "1. item"
        html_node = ordered_list_to_html_node(block)
        self.assertEqual(html_node.tag, "ol")

class TestUnorderedListToHtmlNode(unittest.TestCase):
    def test_unordered_list_to_html_node(self):
        block = "- item"
        html_node = unordered_list_to_html_node(block)
        self.assertEqual(html_node.tag, "ul")
    
if __name__ == "__main__":
    unittest.main()