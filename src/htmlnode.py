class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props != None:
            props = []
            for key,value in self.props.items():
                props.append(f'{key}="{value}"')

            return " ".join(props)
        else:
            return
        
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
         return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)


    def to_html(self):
        if not self.value or self.value == None:
            raise ValueError
        elif not self.tag or self.tag == None:
            return self.value
        else:
            pass