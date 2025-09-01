from textnode import *

def main():
    text_node_one = TextNode("This is some bold text", TextType.BOLD_TEXT)
    text_node_two = TextNode("Picture of a cat", TextType.IMAGE, "https://www.boot.dev")

    text_node_one.__repr__()
    text_node_two.__repr__()

main()