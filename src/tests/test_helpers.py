import unittest

from src.helpers import *
from src.htmlnode import *
from src.htmlnode import *


class TestTextNode(unittest.TestCase):
    def as_pairs(self, nodes):
        return [(n.text, n.text_type) for n in nodes]


    def test_eq(self):
        html_node_one = HTMLNode("a", None, None, {"href": "https://www.google.com","target": "_blank",})
        html_node_two = HTMLNode("a", None, None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(html_node_one, html_node_two)


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images_returns_same_nodes(self):
        node = TextNode("Just plain text, nothing to see.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_single_image_middle(self):
        node = TextNode(
            "Hello ![alt](https://example.com/a.png) world",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" world", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_start_and_end(self):
        node = TextNode(
            "![start](https://e.com/s.png) middle ![end](https://e.com/e.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://e.com/s.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://e.com/e.png"),
            ],
            new_nodes,
        )

    def test_adjacent_images_no_text_between(self):
        node = TextNode(
            "X![a](https://e.com/a.png)![b](https://e.com/b.png)Y",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("X", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://e.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://e.com/b.png"),
                TextNode("Y", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_non_text_nodes_pass_through(self):
        text = TextNode("before ![pic](https://e.com/p.png) after", TextType.TEXT)
        link = TextNode("Click me", TextType.LINK, "https://example.com")
        out = split_nodes_image([text, link])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://e.com/p.png"),
                TextNode(" after", TextType.TEXT),
                link,  # unchanged
            ],
            out,
        )

    def test_multiple_input_nodes(self):
        n1 = TextNode("A ![one](https://e.com/1.png)", TextType.TEXT)
        n2 = TextNode(" + ", TextType.TEXT)
        n3 = TextNode("![two](https://e.com/2.png) B", TextType.TEXT)
        out = split_nodes_image([n1, n2, n3])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://e.com/1.png"),
                TextNode(" + ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://e.com/2.png"),
                TextNode(" B", TextType.TEXT),
            ],
            out,
        )

    def test_ignores_markdown_links_not_images(self):
        node = TextNode(
            "A [link](https://e.com) and ![img](https://e.com/i.png).",
            TextType.TEXT,
        )
        out = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A [link](https://e.com) and ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://e.com/i.png"),
                TextNode(".", TextType.TEXT),
            ],
            out,
        )

    def test_empty_alt_or_url(self):
        node = TextNode(
            "start ![](https://e.com/i.png) mid ![alt]() end",
            TextType.TEXT,
        )
        out = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://e.com/i.png"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, ""),
                TextNode(" end", TextType.TEXT),
            ],
            out,
        )

    def test_no_links_returns_same_nodes(self):
        node = TextNode("No links here, just text.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_links([node]))

    def test_single_link_middle(self):
        node = TextNode("See the [docs](https://example.com) please.", TextType.TEXT)
        out = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("See the ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://example.com"),
                TextNode(" please.", TextType.TEXT),
            ],
            out,
        )

    def test_multiple_links(self):
        node = TextNode(
            "Visit [a](https://a.com) and also [b](https://b.com).",
            TextType.TEXT,
        )
        out = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" and also ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode(".", TextType.TEXT),
            ],
            out,
        )

    def test_adjacent_links_no_space(self):
        node = TextNode(
            "X[a](https://a.com)[b](https://b.com)Y",
            TextType.TEXT,
        )
        out = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("X", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode("Y", TextType.TEXT),
            ],
            out,
        )

    def test_mixed_image_is_ignored_by_link_splitter(self):
        node = TextNode(
            "Img ![alt](https://img.com/i.png) then a [link](https://example.com).",
            TextType.TEXT,
        )
        out = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Img ![alt](https://img.com/i.png) then a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            out,
        )

    def test_pass_through_non_text_nodes(self):
        text = TextNode("Go to [site](https://s.com) now", TextType.TEXT)
        image_node = TextNode("logo", TextType.IMAGE, "https://img.com/logo.png")
        out = split_nodes_links([text, image_node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://s.com"),
                TextNode(" now", TextType.TEXT),
                image_node,
            ],
            out,
        )

    def test_mixed_text_image_link_bold_italic_code(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            out,
        )

    def test_plain_text_no_markup(self):
        text = "Nothing special here."
        out = text_to_textnodes(text)
        self.assertListEqual([TextNode("Nothing special here.", TextType.TEXT)], out)

    def test_unmatched_delimiters_raise(self):
        text = "This **is not closed and _neither is this and `nor code"
        with self.assertRaises(Exception) as ctx:
            text_to_textnodes(text)
        self.assertIn("Unmatched delimiter", str(ctx.exception))

    def test_bold_then_italic_order_inside_bold_not_parsed(self):
        text = "Start **bold and _italic_ inside** end"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold and _italic_ inside", TextType.BOLD_TEXT),
                TextNode(" end", TextType.TEXT),
            ],
            out,
        )

    def test_code_protects_inner_delimiters(self):
        text = "Keep `**not bold** and _not italic_` literal"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Keep ", TextType.TEXT),
                TextNode("**not bold** and _not italic_", TextType.CODE_TEXT),
                TextNode(" literal", TextType.TEXT),
            ],
            out,
        )

    def test_link_text_not_reparsed_by_bold_italic(self):
        text = "Go to [**bold** link](https://ex.com) now"
        out = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("**bold** link", TextType.LINK, "https://ex.com"),
                TextNode(" now", TextType.TEXT),
            ],
            out,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_trims_whitespace(self):
        md = """
    
        First paragraph with spaces   
    
    
        Second one indented
    
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with spaces",
                "Second one indented",
            ],
        )

    def test_markdown_to_blocks_headings_and_lists(self):
        md = """# Heading

        - item one
        - item two

        Final paragraph
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "- item one\n- item two",
                "Final paragraph",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Only one paragraph, no double line breaks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Only one paragraph, no double line breaks."])

    

if __name__ == "__main__":
    unittest.main()

