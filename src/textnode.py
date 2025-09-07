from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic Text_"
    CODE_TEXT = "`Code Text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)" 


class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if not isinstance(other_node, TextNode):
            return False
        return (
            self.text == other_node.text and
            self.text_type == other_node.text_type and
            self.url == other_node.url
        )

    def __repr__(self):
        print(f"TextNode({self.text}, {self.text_type.value}, {self.url})")
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        
