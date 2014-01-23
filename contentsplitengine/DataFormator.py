'''
Created on May 23, 2013

@author: Pahan
'''
from bs4 import BeautifulSoup
from unitgenerator.utilities.PageContentTypes import Text2ContentMapper, Text2ContentMapper2
from transformengine.templategenerator.structures import BlogArticle

class DataFormator():

    data = None
    soup = None
    # nonTextTags = ["img","a"]

    def __init__(self, content):
        self.data = content
        self.soup = BeautifulSoup(self.data)
        
    def getFormattedData(self):
        
        article = BlogArticle()
        parenttagname = ""
        tagname = ""
        tagChanged = False
        text = ""
        for child in self.soup.recursiveChildGenerator():
            
            name = getattr(child, "name", None)
            if name is not None:
                parenttagname = tagname
                tagname = name
                if Text2ContentMapper.has_key(name):
                    if not text is "":
                        article.addContent("text", "", text.rstrip())
                        text = ""
                    self.getNonTextData(child, article)
                    
                tagChanged = True
            elif not child.isspace():  # leaf node, don't print spaces
                tagChanged = not tagChanged
                tagg = None
                if (tagChanged):
                    tagg = parenttagname
                else:
                    tagg = tagname
                if not Text2ContentMapper2.has_key(tagg):
                    text = text + child
        return article
                
                    
    def getNonTextData(self, node, barticle):
        mapattr = Text2ContentMapper[node.name]
        if mapattr == 'h':
            barticle.addContent(node.name, '', node.get_text())
        elif not mapattr is '':
#             barticle.addContent(node.name, node[mapattr], node.get_text())
            atrb = node[mapattr] if node.has_attr(mapattr) else ''
            barticle.addContent(node.name, atrb, node.get_text())
        
        else:
            barticle.addContent(node.name, "", "")
            
