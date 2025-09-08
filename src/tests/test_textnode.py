import unittest

from src.textnode import *
from src.htmlnode import *
from src.helpers import *


class TestTextNode(unittest.TestCase):    
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




if __name__ == "__main__":
    unittest.main()

