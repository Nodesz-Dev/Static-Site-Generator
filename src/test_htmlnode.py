import unittest

from htmlnode import HTMLNode

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
