
class HTMLNode:
    def __init__(self, tag: str = None , value: str=None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
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


