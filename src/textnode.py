from enum import Enum

class TextType(Enum):
    text = "text"
    bold = "bold_text"
    italic = "italic_text"
    code = "code"
    links = "links"
    images = "images"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if self.text != node.text:
            return False
        if self.text_type != node.text_type:
            return False
        if self.url != node.url:
            return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



