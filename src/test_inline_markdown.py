import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import *

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_node_delimiter(self):
        # Test splitting a node with a code block delimiter.
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result,expected)

    def test_split_nodes_delimiter_empty_input(self):
        # Test case: Empty input list of nodes.
        nodes = []
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_split_nodes_delimiter_no_delimiter(self):
        # Test case: No delimiter found in the input.
        nodes = [TextNode("hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_single_delimiter(self):
        # Test case: Single delimiter in the input.
        nodes = [TextNode("hello**world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("hello", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        # Test case: Multiple delimiters in the input.
        nodes = [TextNode("hello**world**again", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("hello", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("again", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_adjacent_delimiters(self):
        # Test case: Adjacent delimiters in the input.
        nodes = [TextNode("hello****world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("hello", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode("world", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_different_texttype(self):
        # Test case: Different texttype delimiter.
        nodes = [TextNode("hello__world__again", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "__", TextType.ITALIC)
        expected = [
            TextNode("hello", TextType.TEXT),
            TextNode("world", TextType.ITALIC),
            TextNode("again", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_existing_bold_node(self):
        # Test case: Existing bold node in the input.
        nodes = [TextNode("hello", TextType.TEXT), TextNode("world", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("hello", TextType.TEXT), TextNode("world", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_delimiter_at_start_of_text(self):
        # Test case: delimiter at the beginning of the text value
        nodes = [TextNode("****hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("", TextType.TEXT),TextNode("", TextType.BOLD),TextNode("hello world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_delimiter_at_end_of_text(self):
        #Test case: delimiter at the end of the text value
        nodes = [TextNode("hello world****", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("hello world", TextType.TEXT),TextNode("",TextType.BOLD),TextNode("",TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_consecutive_delimiters(self):
        #Test case: 3 sets of delimiter in sequence
        nodes = [TextNode("hello ******** world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("hello ", TextType.TEXT),
                    TextNode("", TextType.BOLD), 
                    TextNode("", TextType.TEXT), 
                    TextNode("", TextType.BOLD), 
                    TextNode(" world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        #Test case: Empty string value
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

class TestMarkdownExtractImages(unittest.TestCase):
    def test_extract_markdown_basic_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, matches)

    def test_extract_spaces_in_alt_text_and_url(self):
        matches = extract_markdown_images(
            "This is text with an ![ ima ge](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [(" ima ge", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(matches, expected)

    def test_extract_parentheses_in_alt_text_and_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https:// i.img ur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https:// i.img ur.com/zjjcJKZ.png")]
        self.assertListEqual(matches, expected)

    def test_extract_multiple_image_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). Oh shit another one ![image2](https://i.imgur.com/second.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/second.png")]
        self.assertListEqual(matches, expected)

    def test_extract_no_image_link(self):
        matches = extract_markdown_images(
            "This is text with an image"
        )
        expected = []
        self.assertListEqual(matches, expected)

    def test_extract_special_characters(self):
        matches = extract_markdown_images(
            "This is text with an ![i_m?a,g=e&](https://i.imgur.com/_-.?=&.png)"
        )
        expected = [("i_m?a,g=e&","https://i.imgur.com/_-.?=&.png")]
        self.assertListEqual(matches, expected)

    def test_extract_empty_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("","https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, matches)

    def test_extract_empty_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image]()"
        )
        expected = [("image","")]
        self.assertListEqual(expected, matches)

    def test_extract_mix_valid_and_invalid(self):
        matches = extract_markdown_images(
            "This is text with an ![(https://i.imgur.com/zjjcJKZ.png). another one ![image2](https://i.imgur.com/image2.png) another one ![image3]()"
        )
        expected = [("image2","https://i.imgur.com/image2.png"),("image3","")]
        self.assertListEqual(expected, matches)

class TestMarkdownExtractLink(unittest.TestCase):
    def test_extract_markdown_basic_link(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(expected, matches)

    def test_extract_spaces_in_link_text(self):
        matches = extract_markdown_links(
            "This is text with an [link tex t](https://link.com)"
        )
        expected = [("link tex t", "https://link.com")]
        self.assertListEqual(expected, matches)

    def test_extract_spaces_in_url(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://l ink.c om)"
        )
        expected = [("link", "https://l ink.c om")]
        self.assertListEqual(expected, matches)

    def test_extract_parentheses_in_link_and_url(self):
        matches = extract_markdown_links(
            "This is text with an [l(i)nk](https://l(i)nk.com)"
        )
        expected = []
        self.assertListEqual(expected, matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://link1.com) another one [link2](https://link2.com)"
        )
        expected = [("link1", "https://link1.com"),("link2","https://link2.com")]
        self.assertListEqual(expected, matches)
    
    def test_extract_no_links(self):
        matches = extract_markdown_links(
            "This is text without a link"
        )
        expected = []
        self.assertListEqual(expected, matches)

    def test_extract_special_characters(self):
        matches = extract_markdown_links(
            "This is text with an [li*-_?nk](https://li*-_?nk.com)"
        )
        expected = [("li*-_?nk", "https://li*-_?nk.com")]
        self.assertListEqual(expected, matches)

    def test_extract_empty_link_text(self):
        matches = extract_markdown_links(
            "This is text with an [](https://link.com)"
        )
        expected = [("", "https://link.com")]
        self.assertListEqual(expected, matches)

    def test_extract_empty_url(self):
        matches = extract_markdown_links(
            "This is text with an [link]()"
        )
        expected = [("link","")]
        self.assertListEqual(expected, matches)

    def test_extract_mix_valid_and_invalid(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://link.com) another one [link2]() final one [link3](https://link3.com)"
        )
        expected = [("link", "https://link.com"),("link2", ""),("link3","https://link3.com")]
        self.assertListEqual(expected, matches)

    def test_extract_image_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = []
        self.assertListEqual(expected, matches)

class TestMarkdownSplitNodesImages(unittest.TestCase):
        def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            expected = [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
                ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_text_at_end(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) extra text",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            expected = [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                    TextNode(" extra text", TextType.TEXT)
                ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_no_images(self):
            node = TextNode("This is a text without an image", TextType.TEXT)
            new_nodes = split_nodes_image([node])
            expected = [TextNode("This is a text without an image", TextType.TEXT)]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_image_at_start(self):
            node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) Image at start", TextType.TEXT)
            new_nodes = split_nodes_image([node])
            expected = [
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" Image at start", TextType.TEXT)
            ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_adjacent_images(self):
            node = TextNode("this is text with two ![image](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur2.com/zjjcJKZ.png)", TextType.TEXT)
            new_nodes = split_nodes_image([node])
            expected = [
                    TextNode("this is text with two ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE,"https://i.imgur.com/zjjcJKZ.png"),
                    TextNode("image2",TextType.IMAGE,"https://i.imgur2.com/zjjcJKZ.png")
            ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_empty_alt_text(self):
            node = TextNode("this is text with empty alt text ![](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            new_nodes = split_nodes_image([node])
            expected = [
                    TextNode("this is text with empty alt text ", TextType.TEXT),
                    TextNode("", TextType.IMAGE,"https://i.imgur.com/zjjcJKZ.png")
            ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_empty_url(self):
            node = TextNode("this is text with empty url ![image]()", TextType.TEXT)
            new_nodes = split_nodes_image([node])
            expected = [
                    TextNode("this is text with empty url ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE,"")
            ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_existing_non_text_nodes(self):
            node = [TextNode("hello", TextType.BOLD), TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
            new_nodes = split_nodes_image(node)
            expected = [
                    TextNode("hello", TextType.BOLD),
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ]
            self.assertListEqual(expected,new_nodes)

        def test_split_images_special_characters(self):
            node = TextNode(
                "This is text with an ![im*-_?age](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.im*-_?gur.com/3elNhQu.png)",
                TextType.TEXT
                )
            new_nodes = split_nodes_image([node])
            expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("im*-_?age", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.im*-_?gur.com/3elNhQu.png")
            ]
            self.assertListEqual(expected,new_nodes)

class TestMarkdownSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://example.com) and another [second link](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example2.com")
            ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_text_at_end(self):
        node = TextNode(
            "This is text with an [link](https://example.com) and another [second link](https://example2.com) extra text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example2.com"),
                TextNode(" extra text", TextType.TEXT)
            ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("This is a text without a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is a text without a link", TextType.TEXT)
        ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_image_at_start(self):
        node = TextNode("[link](https://example.com) Image at start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" Image at start", TextType.TEXT)
        ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_adjacent_images(self):
        node = TextNode("this is text with two [link](https://example.com)[link2](https://example2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("this is text with two ", TextType.TEXT),
                TextNode("link", TextType.LINK,"https://example.com"),
                TextNode("link2",TextType.LINK,"https://example2.com")
        ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_empty_alt_text(self):
        node = TextNode("this is text with empty alt text [](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("this is text with empty alt text ", TextType.TEXT),
                TextNode("", TextType.LINK,"https://example.com")
        ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_empty_url(self):
        node = TextNode("this is text with empty url [link]()", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
                TextNode("this is text with empty url ", TextType.TEXT),
                TextNode("link", TextType.LINK,"")
        ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_existing_non_text_nodes(self):
        node = [TextNode("hello", TextType.BOLD), TextNode("This is text with an [link](https://example.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(node)
        expected = [
                TextNode("hello", TextType.BOLD),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertListEqual(expected,new_nodes)

    def test_split_images_special_characters(self):
        node = TextNode(
            "This is text with an [li*-_?nk](https://example.com) and another [second link](https://ex*-_?ample.com)",
            TextType.TEXT
            )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("li*-_?nk", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://ex*-_?ample.com")
        ]
        self.assertListEqual(expected,new_nodes)

class TestMarkdownTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is plain text.", TextType.TEXT)
            ]
        self.assertListEqual(expected,new_nodes)

    def test_text_to_textnodes_bold_text(self):
        text = "This is **bold** text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_italic_text(self):
        text = "This is _italic_ text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_code_text(self):
        text = "This is `code` text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("code", TextType.CODE), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_image(self):
        text = "This is ![alt text](image.jpg) text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("alt text", TextType.IMAGE, "image.jpg"), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_link(self):
        text = "This is [link text](https://example.com) text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("link text", TextType.LINK, "https://example.com"), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_multiple_formats(self):
        text = "This is **bold** and _italic_ and `code` and ![alt text](image.jpg) and [link text](https://example.com) text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("code", TextType.CODE), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("alt text", TextType.IMAGE, "image.jpg"), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("link text", TextType.LINK, "https://example.com"), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_nested_formats(self):
        text = "This is **bold _italic_ bold** text."
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("bold ", TextType.BOLD), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" bold", TextType.BOLD), 
            TextNode(" text.", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()