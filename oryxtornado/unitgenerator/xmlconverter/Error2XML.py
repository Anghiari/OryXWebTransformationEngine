'''
Created on Jun 5, 2013

@author: acer
'''
import xml.etree.ElementTree as ET
from unitgenerator.utilities.PageContentTypes import Text2ContentMapper

class Error2XML():

    errorobj = None
    
    def __init__(self, errorobject):
        self.errorobj = errorobject
        
    def generateXML(self):
        
#        article = ET.Element("HTTP")
#        acontent = ET.SubElement(article, "content")
#        for _ in xrange(self.blogarticle.get_length()):
#            c = self.blogarticle.get_item()
#            field = ET.SubElement(acontent, "item")
#            field.set("tag", c.get_tag())
#            if c.get_attr():
#                field.set("attr", Text2ContentMapper[c.get_tag()])
#                field.set("attrVal",c.get_attr())
#            field.text = c.get_text()
#        tree = ET.ElementTree(article)
#        
#        return tree
#        
