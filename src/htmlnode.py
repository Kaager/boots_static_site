
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_string = ""

        if not self.props:
            return html_string

        for item in self.props.keys():
            html_string += f' {item}="{self.props[item]}"'
        return html_string
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("'valuu' needs an actual value")
    
        if not self.tag:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Props: {self.props}"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("'tag' can't be None")
        if self.children is None:
            raise ValueError("no children for this parent")
        
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"