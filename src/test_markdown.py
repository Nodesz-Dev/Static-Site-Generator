import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()