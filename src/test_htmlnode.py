import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"href":"https",
                                "hi":"test",})
        node2 = HTMLNode(props={"1": "2",
                                "3": "4",
                                "5": "6",
                                "7":"8",
                                "9":"10"})
        node3 = HTMLNode(tag="lol", props={1:2,
                                           3:4,
                                           (5,6):(7,8)})
        
        self.assertEqual(node1.props_to_html(), ' href="https" hi="test"')
        self.assertEqual(node2.props_to_html(), ' 1="2" 3="4" 5="6" 7="8" 9="10"')
        self.assertEqual(node3.props_to_html(), ' 1="2" 3="4" (5, 6)="(7, 8)"')

    def test_html_node_repr(self):
        node1 = HTMLNode(tag="lol", props={1:2,
                                           3:4,
                                           (5,6):(7,8)})
        node1_repr = 'HTMLNode Class (Tag: lol, Value: None, Children: None, Props: {1: 2, 3: 4, (5, 6): (7, 8)})'
        
        self.assertEqual(repr(node1), node1_repr)

    def test_leaf_to_html_p(self):
        node1 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("p", "Hello, world! - but with props", {"href": "www.google.com"})
        self.assertEqual(node2.to_html(), '<p href="www.google.com">Hello, world! - but with props</p>')

    def test_leaf_to_html_a(self):
        node1 = LeafNode("a", "Click me!", {"href": "www.google.com"})
        self.assertEqual(node1.to_html(), '<a href="www.google.com">Click me!</a>')

        node2 = LeafNode("a", "Click me!", {"yaya": "www.yahoo.com"})
        self.assertEqual(node2.to_html(), '<a yaya="www.yahoo.com">Click me!</a>')

        node3 = LeafNode("a", "Click me! - two props", {"yaya": "www.yahoo.com", "href":"www.google.com"})
        self.assertEqual(node3.to_html(), '<a yaya="www.yahoo.com" href="www.google.com">Click me! - two props</a>')

    def test_left_to_html_no_tage(self):
        node1 = LeafNode(None, "No Tag - Just Text")
        self.assertEqual(node1.to_html(), "No Tag - Just Text")

        node2 = LeafNode(None, "No Tag - Just text - with a side of unused props", {"href":"www.bing.com"})
        self.assertEqual(node2.to_html(), "No Tag - Just text - with a side of unused props")

