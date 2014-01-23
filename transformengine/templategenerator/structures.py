'''
Created on Jun 5, 2013

@author: acer
'''

from collections import deque
from transformengine.contenttypes.BlogArticleContent import BlogArticleContent


class BlogArticle():

    blogContent = deque()
    
    def __init__(self):
        self.blogContent = deque()
        
    def addContent(self, tag, attr, text):
        content = BlogArticleContent(tag, attr, text)
        self.blogContent.append(content)        
        
    def getBlogArticle(self):
        return self.blogContent
    
    def get_length(self):
        return len(self.blogContent)
    
    def get_item(self):
        return self.blogContent.popleft()
    
    
class ErrorMessage():

    message=""
    code=0
    

    def __init__(self,code,message):
        self.message=message 
        self.code=code
        
    def setMessage(self,msg):
        self.message=msg 
        
    def getMessage(self):
        return self.message
    
    
    def setCode(self,code):
        self.message=code
        
    def getCode(self):
        return self.code
    
    
    