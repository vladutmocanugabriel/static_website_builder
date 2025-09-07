import unittest

from src.textnode import *
from src.htmlnode import *
from src.helpers import *


class TestTextNode(unittest.TestCase):
    def as_pairs(self, nodes):
        return [(n.text, n.text_type) for n in nodes]
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_eq_image_type(self):
        node = TextNode("This is an image node", TextType.IMAGE)
        node2 = TextNode("This is an image node", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_url_default_value(self):
        node = TextNode("This is an image node", TextType.IMAGE)
        self.assertEqual(node.url, None)

    def test_url_set_value(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://bootdev.com")
        self.assertEqual(node.url, "https://bootdev.com")

    def test_nodes_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_anchor(self):
        node = TextNode("This is a <a> node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a <a> node")

    def test_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")

    def test_code_simple(self):
        nodes = [TextNode("This has `code` inside.", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(
            self.as_pairs(out),
            [
                ("This has ", TextType.TEXT),
                ("code", TextType.CODE_TEXT),
                (" inside.", TextType.TEXT),
            ],
        )

    def test_code_multiple(self):
        nodes = [TextNode("pre `one` mid `two` post", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(
            self.as_pairs(out),
            [
                ("pre ", TextType.TEXT),
                ("one", TextType.CODE_TEXT),
                (" mid ", TextType.TEXT),
                ("two", TextType.CODE_TEXT),
                (" post", TextType.TEXT),
            ],
        )

    def test_code_leading_and_trailing(self):
        nodes = [TextNode("`start` middle `end`", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(
            self.as_pairs(out),
            [
                ("start", TextType.CODE_TEXT),
                (" middle ", TextType.TEXT),
                ("end", TextType.CODE_TEXT),
            ],
        )

    def test_code_plain_only(self):
        nodes = [TextNode("no code here", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(self.as_pairs(out), [("no code here", TextType.TEXT)])

    def test_code_empty_segment_is_kept_for_delimited(self):
        nodes = [TextNode("before `` after", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(
            self.as_pairs(out),
            [
                ("before ", TextType.TEXT),
                ("", TextType.CODE_TEXT),
                (" after", TextType.TEXT),
            ],
        )

    def test_pass_through_non_text(self):
        nodes = [TextNode("already bold", TextType.BOLD_TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        self.assertEqual(self.as_pairs(out), [("already bold", TextType.BOLD_TEXT)])


if __name__ == "__main__":
    unittest.main()

