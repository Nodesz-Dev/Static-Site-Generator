

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return_string = ""
        for key, value in self.props.items():
            return_string += f' {key}="{value}"'

        return return_string
    
    def __repr__(self):
        return f"HTMLNode Class (Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"