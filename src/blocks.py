from enum import Enum
import re
from enum import Enum
import re
from src.helpers import text_node_to_html_node, text_to_textnodes, markdown_to_blocks
from src.htmlnode import ParentNode
from src.textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block_markdown):
    if re.match(r"^#{1,6} ", block_markdown):
        return BlockType.HEADING
    elif block_markdown.startswith("```") and block_markdown.endswith("```"):
        return BlockType.CODE
    elif block_markdown.startswith(">"):
        lines = block_markdown.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE       
    elif block_markdown.startswith("1. "):
        lines = block_markdown.split("\n")
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    elif block_markdown.startswith("- "):
        lines = block_markdown.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            parent_node.children.append(ParentNode("p", children))

        elif block_type == BlockType.HEADING:
            m = re.match(r'^(#{1,6})\s+(.*)$', block)
            if not m:
                children = text_to_children(block)
                parent_node.children.append(ParentNode("p", children))
                continue
            level = len(m.group(1))
            heading_text = m.group(2)
            children = text_to_children(heading_text)
            parent_node.children.append(ParentNode(f"h{level}", children))

        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            code_text = "\n".join(lines)

            code_leaf = text_node_to_html_node(TextNode(code_text, TextType.CODE_TEXT))
            parent_node.children.append(ParentNode("pre", [code_leaf]))

        elif block_type == BlockType.QUOTE:
            quote_lines = []
            for line in block.split("\n"):
                quote_lines.append(re.sub(r'^\>\s?', '', line))
            quote_text = "\n".join(quote_lines)
            children = text_to_children(quote_text)
            parent_node.children.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            ul_children = []
            for line in block.split("\n"):
                item_text = re.sub(r'^\-\s+', '', line)
                li_children = text_to_children(item_text)
                ul_children.append(ParentNode("li", li_children))
            parent_node.children.append(ParentNode("ul", ul_children))

        elif block_type == BlockType.ORDERED_LIST:
            ol_children = []
            lines = block.split("\n")
            for i, line in enumerate(lines):
                item_text = re.sub(rf'^{i+1}\.\s+', '', line)
                li_children = text_to_children(item_text)
                ol_children.append(ParentNode("li", li_children))
            parent_node.children.append(ParentNode("ol", ol_children))

        else:
            children = text_to_children(block)
            parent_node.children.append(ParentNode("p", children))

    return parent_node










    