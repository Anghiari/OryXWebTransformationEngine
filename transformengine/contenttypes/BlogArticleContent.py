'''
Created on May 22, 2013

@author: Pahan
'''

class BlogArticleContent():
    
    tag = None
    attr = None
    text = None
    
    def __init__(self, tag, attr, text):
        self.tag = tag
        self.attr = attr
        self.text = text    

    def get_tag(self):
        return self.tag


    def get_attr(self):
        return self.attr


    def get_text(self):
        return self.text

        
        
