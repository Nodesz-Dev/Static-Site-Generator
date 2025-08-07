import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()