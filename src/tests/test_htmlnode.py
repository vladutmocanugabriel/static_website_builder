import unittest

from src.htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()

