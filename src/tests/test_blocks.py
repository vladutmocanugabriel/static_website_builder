import unittest
import re

from src.blocks import *

def _minify(html: str) -> str:
    """Helper to ignore insignificant whitespace differences."""
    return re.sub(r"\s+", "", html)


class TestTextNode(unittest.TestCase):    
    def test_heading_level_1(self):
        self.assertEqual(
            block_to_block_type("# Title"),
            BlockType.HEADING
        )

    def test_heading_level_6(self):
        self.assertEqual(
            block_to_block_type("###### Deep Title"),
            BlockType.HEADING
        )

    def test_code_block_single_line_fenced(self):
        self.assertEqual(
            block_to_block_type("```print('hi')```"),
            BlockType.CODE
        )

    def test_code_block_multiline_fenced(self):
        code = "```\nline1\nline2\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_all_lines_prefixed(self):
        quote = "> a\n> b\n> c"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_quote_invalid_falls_to_paragraph(self):
        mixed = "> a\nnot quote\n> c"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_unordered_list_simple(self):
        ul = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_falls_to_paragraph(self):
        mixed = "- item 1\nx item 2\n- item 3"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_ordered_list_incrementing(self):
        ol = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_numbering_falls_to_paragraph(self):
        bad = "1. one\n3. three"
        self.assertEqual(block_to_block_type(bad), BlockType.PARAGRAPH)

    def test_paragraph_plain_text(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph of text."),
            BlockType.PARAGRAPH
        )

    def test_not_heading_without_space_after_hash(self):
        self.assertEqual(
            block_to_block_type("#NoSpace"),
            BlockType.PARAGRAPH
        )

    def test_heading_with_inline(self):
        md = "# Title with **bold** and _italic_ and a [link](https://ex.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """
        <div>
          <h1>
            Title with <b>bold</b> and <i>italic</i> and a
            <a href="https://ex.com">link</a>
          </h1>
        </div>
        """
        self.assertEqual(_minify(html), _minify(expected))

    def test_codeblock_keeps_literals(self):
        md = "```\ncode **not bold** and _not italic_ and [not a link](#)\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """
        <div>
          <pre><code>code **not bold** and _not italic_ and [not a link](#)</code></pre>
        </div>
        """
        self.assertEqual(_minify(html), _minify(expected))

    def test_blockquote_with_inline(self):
        md = "> quoted **bold** text\n> and _italic_ with a [link](https://ex.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """
        <div>
          <blockquote>
            quoted <b>bold</b> text
            and <i>italic</i> with a <a href="https://ex.com">link</a>
          </blockquote>
        </div>
        """
        self.assertEqual(_minify(html), _minify(expected))


    def test_ordered_list_with_inline(self):
        md = "1. first has **bold**\n2. second has _italic_ and a [link](https://ex.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """
        <div>
          <ol>
            <li>first has <b>bold</b></li>
            <li>second has <i>italic</i> and a <a href="https://ex.com">link</a></li>
          </ol>
        </div>
        """
        self.assertEqual(_minify(html), _minify(expected))




if __name__ == "__main__":
    unittest.main()