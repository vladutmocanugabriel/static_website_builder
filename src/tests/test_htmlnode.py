import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        html_node_one = HTMLNode("a", None, None, {"href": "https://www.google.com","target": "_blank",})
        html_node_two = HTMLNode("a", None, None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(html_node_one, html_node_two)

    def test_not_eq(self):
        html_node_one = HTMLNode("a", None, None, None)
        html_node_two = HTMLNode("a", None, None, {"href": "https://www.google.com","target": "_blank",})
        self.assertNotEqual(html_node_one, html_node_two)

    def test_props_to_html(self):
        html_node_one = HTMLNode("a", None, None, {"href": "https://www.google.com","target": "_blank",})
        repr_hmtl_node = html_node_one.__repr__()
        self.assertEqual(f"HTMLNode({html_node_one.tag}, {html_node_one.value}, {html_node_one.children}, {html_node_one.props_to_html()})", repr_hmtl_node)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_a_without_props(self):
        node = LeafNode("a", "Click me!")
        self.assertEqual(node.to_html(), '<a>Click me!</a>')

    def test_leaf_to_html_a_without_tag(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), 'Click me!')

    def test_leaf_to_html_a_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("a", None).to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_more_children(self):
        child_node_one = LeafNode("b", "Bold text")
        child_node_two = LeafNode(None, "Normal text")
        child_node_three = LeafNode("i", "italic text")
        child_node_four = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node_one,child_node_two,child_node_three,child_node_four])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


if __name__ == "__main__":
    unittest.main()

