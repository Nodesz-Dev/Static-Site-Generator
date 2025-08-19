import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_equal_nodes(self):
        # Test that two TextNodes with the same text and type are equal
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_equal_nodes_different_text(self):
        # Test that two TextNodes with different text are not equal
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node ", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_nodes_different_type(self):
        # Test that two TextNodes with different types are not equal
        node1 = TextNode("This is a text node ", TextType.BOLD)
        node2 = TextNode("This is a text node ", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_not_equal_nodes_different_link(self):
        # Test that two TextNodes with different links are not equal
        node1 = TextNode("This is a text node ", TextType.CODE)
        node2 = TextNode("This is a text node ", TextType.CODE, "https")
        self.assertNotEqual(node1, node2)

    def test_equal_nodes_same_link(self):
        # Test that two TextNodes with the same link are equal
        node1 = TextNode("This is a text node ", TextType.CODE, "https")
        node2 = TextNode("This is a text node ", TextType.CODE, "https")
        self.assertEqual(node1, node2)

    def test_none_node_values_equal(self):
        # Test that two nodes with none values are equal
        node1 = TextNode(None, TextType.TEXT, None)
        node2 = TextNode(None, TextType.TEXT)
        self.assertEqual(node1, node2)

class TestTestNodeToHTML(unittest.TestCase):
    def test_text(self):
        # Test converting a TEXT TextNode to an HTMLNode
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        # Test converting a BOLD TextNode to an HTMLNode
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_code(self):
        # Test converting a code TextNode to an HTMLNode
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_italic(self):
        # Test converting a italic TextNode to an HTMLNode
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_link(self):
        # Test converting a link TextNode to an HTMLNode
        node = TextNode("This is a link node", TextType.LINK, "link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "link"})

    def test_image(self):
        # Test converting an IMAGE TextNode to an HTMLNode
        node = TextNode("This is an image", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "www.image.com", "alt": "This is an image"})

    def test_special_characters_in_text(self):
        # Test converting a TextNode with special characters in the text value
        node = TextNode("Special Characters!?*", TextType.TEXT)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "Special Characters!?*")

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

if __name__ == "__main__":
    unittest.main()