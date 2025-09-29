import os, shutil
import re
import os, shutil
import re
from src.htmlnode import LeafNode
from src.textnode import TextType, TextNode


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
        # value=None; use attributes for src/alt
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        
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

def clean_public(public_path):
    if not os.path.exists(public_path):
        os.mkdir(public_path)
        print(f"You're missing the public folder so we created it for you: {public_path}")
    elif os.listdir(public_path):
        for filename in os.listdir(public_path):
            file_path = os.path.join(public_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                print(f"{file_path} has just been removed.")
            elif os.path.isdir(file_path):
                print(f"{file_path} folder and all it's content has just been removed")
                shutil.rmtree(file_path) 

def copy_to_public(source, destination):
    for entry in os.listdir(source):
        entry_path = os.path.join(source, entry)
        if os.path.isdir(entry_path):
            new_public_path = os.path.join(destination, entry)
            os.mkdir(new_public_path)
            copy_to_public(entry_path, new_public_path)
        elif os.path.isfile(entry_path):
            shutil.copy2(entry_path, destination)

        
            