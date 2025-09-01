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
        text_equals = self.text == other_node.text
        text_type_equals = self.text_type == other_node.text_type
        url_equals = self.url == other_node.url

        if text_equals and text_type_equals and url_equals:
            return True
        else:
            return False

    def __repr__(self):
        print(f"TextNode({self.text}, {self.text_type.value}, {self.url})")
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"