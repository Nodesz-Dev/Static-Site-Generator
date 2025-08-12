import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node ", TextType.BOLD)
        self.assertNotEqual(node, node3)

        node4 = TextNode("This is a text node ", TextType.CODE)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("This is a text node ", TextType.CODE, "https")
        self.assertNotEqual(node4, node5)

        node6 = TextNode("This is a text node ", TextType.CODE, "https")
        self.assertEqual(node5, node6)

class TestTestNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "www.image.com", "alt": "This is an image"})


if __name__ == "__main__":
    unittest.main()