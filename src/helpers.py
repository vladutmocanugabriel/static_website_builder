from src.htmlnode import HTMLNode, LeafNode, ParentNode
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
        

        

            