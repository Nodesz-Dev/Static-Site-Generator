

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        return_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                return_string += f' {key}="{value}"'

        return return_string
    
    def __repr__(self):
        return f"HTMLNode Class (Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            print(self)
            raise ValueError("Value Missing: Leaf node is required to have a value")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: Tag is required")
        if self.children is None:
            raise ValueError("Error: Children are required")
        
        children_string = ""
        for child in self.children:
            children_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"