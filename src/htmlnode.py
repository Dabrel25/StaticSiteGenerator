

class HTMLNode:
    def __init__(self, tag: str = None , value: str=None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        props_strings = ""
        if self.props:
            for k, v in self.props.items():
                props_strings +=  f' {k}="{v}"'
            return props_strings
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"