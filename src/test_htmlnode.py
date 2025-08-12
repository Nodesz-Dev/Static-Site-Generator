import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><p>child2</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_different_tree_depths(self):
        node_right_grandchild = LeafNode("b", "right grandchild")
        node_right_child = ParentNode("span", [node_right_grandchild])

        node_left_child1 = LeafNode("a", "left child1", {"href": "www.child1.com"})
        node_left_child2 = LeafNode("p", "left child2")

        parent_node = ParentNode("span", [node_left_child1, node_left_child2, node_right_child])

        self.assertEqual(parent_node.to_html(), f'<span><a href="www.child1.com">left child1</a><p>left child2</p><span><b>right grandchild</b></span></span>')

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.to_html(), "<p></p>")

    def test_to_html_with_no_child_value(self):
        parent_node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError, "Error: Children are required"):
            temp = parent_node.to_html()

    def test_to_html_with_no_tag_value(self):
        parent_node = ParentNode(None, "Child")
        with self.assertRaisesRegex(ValueError, "Error: Tag is required"):
            parent_node.to_html()

   

    


if __name__ == "__main__":
    unittest.main()