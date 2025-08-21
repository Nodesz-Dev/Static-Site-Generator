import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

if __name__ == "__main__":
    unittest.main()