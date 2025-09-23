from textnode import TextNode,TextType

# python
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children  # keep None if not provided
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        if self.tag == "img":
            return f'<img{self.props_to_html()}/>'
        inner = ""
        if self.children:
            inner = "".join(child.to_html() for child in self.children)
        elif self.value is not None:
            inner = self.value
        return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"
    def props_to_html(self):
        props_strings = ""
        if not self.props:
            return ""
        for k, v in self.props.items():
            props_strings +=  f' {k}="{v}"'
        return props_strings

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no value")
        if self.tag is None:
            return f"{self.value}"
        attrs = self.props_to_html()
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode("a",text_node.text, props= {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
    raise Exception('TextType is not valid.')




