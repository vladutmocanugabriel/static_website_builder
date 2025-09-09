import re
from src.htmlnode import *
from src.textnode import *

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError(f"Unknown text type: {text_node.text_type}")
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text) 
    if text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Unmatched delimiter")
        
        for i,part in enumerate(parts):
            if i%2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                    continue
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if len(extract_markdown_images(node.text)) == 0:
                new_nodes.append(node)
            else:
                parts = extract_markdown_images(node.text)
                remaining = node.text
                for part in parts:
                    sections =remaining.split(f"![{part[0]}]({part[1]})", 1)
                    if len(sections[0]) != 0:
                        new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    
                    new_nodes.append(TextNode(part[0], TextType.IMAGE, part[1]))
                    remaining = sections[1]
                
                if len(remaining) != 0:
                    new_nodes.append(TextNode(remaining,TextType.TEXT))
        else:
            new_nodes.append(node)
        
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = extract_markdown_links(node.text)
            if not parts:
                new_nodes.append(node)
                continue

            remaining = node.text
            for text, url in parts:
                sections = remaining.split(f"[{text}]({url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                remaining = sections[1]
            if len(remaining) != 0:
                new_nodes.append(TextNode(remaining, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    return nodes
        

def markdown_to_blocks(markdown):
    blocks = re.split(r"\n\s*\n+", markdown)
    cleaned = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = [line.strip() for line in block.split("\n")]
        cleaned.append("\n".join(lines))
    return cleaned


            