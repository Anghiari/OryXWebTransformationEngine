import re
import xml.etree.ElementTree as ET
from unitgenerator.utilities.PageContentTypes import Text2ContentMapper
import constants.Constants as const
from bs4 import BeautifulSoup
from HTMLStripper import strip_tags

class Blog2XML():

    
    blogarticle = None
    
    def __init__(self,bloga):
        self.blogarticle = bloga
        
    def generateXML(self, statuscode, favicon='', mobileurl=''):
        
        oryx=ET.Element("oryx")
         
        http=ET.SubElement(oryx,"HTTP")
        code=ET.SubElement(http,"code")
        code.text=str(statuscode)
         
        #A error message should be printed here - to do
        message=ET.SubElement(http,"message")
        if(statuscode == const.HAS_MOBILE_SITE):
            message.text = mobileurl
        else:
            message.text=const.messages.get(statuscode, 'Unkonwn Error Code!')
            
        tree = ET.ElementTree(oryx)
        
        if(statuscode==const.HTTP_OK):
            fav = ET.SubElement(oryx,"favicon")
            fav.text = favicon
            article = ET.SubElement(oryx,"article")
            acontent = ET.SubElement(article, "content")
            for _ in xrange(self.blogarticle.get_length()):
                c = self.blogarticle.get_item()
                field = ET.SubElement(acontent, "item")
                field.set("tag", c.get_tag())
                if c.get_attr():
                    field.set("attr", Text2ContentMapper[c.get_tag()])
                    field.set("attrVal",c.get_attr())
                field.text = c.get_text()            
        
        return tree
    
    def generateTileXML(self, blogTitle, feed, favicon=''):
        
        oryx = ET.Element("oryx")
        info = ET.SubElement(oryx,"info")
        
        blogname = ET.SubElement(info,"blogname")
        blogname.text = str(blogTitle)
        fav = ET.SubElement(info,"favicon")
        fav.text = favicon
        
        post = ET.SubElement(oryx,"post")
        
        for entry in feed['entries']:
            item = ET.SubElement(post,"item")
            
            pubDate = ET.SubElement(item,"published")
            title = ET.SubElement(item,"title")
            link = ET.SubElement(item,"link")
            image = ET.SubElement(item,"image")
            summary = ET.SubElement(item,"summary")
            
            pubDate.text = entry['published']
            title.text = entry['title']
            link.text = entry['link']
            summary.text = self.extractTextFromHTML(entry['summary'])
            image.text = self.extractBestImage(entry['summary'])
            
        return ET.ElementTree(oryx)
    
    def extractTextFromHTML(self, html):
        return strip_tags(html)
        
    def extractBestImage(self, html):
        soup = BeautifulSoup(html)
        imgs = soup.findAll('img')
        for img in imgs:
            w = int(re.match(r'\d+', img.attrs['width']).group() if 'width' in img.attrs else -1)
            h = int(re.match(r'\d+', img.attrs['height']).group() if 'height' in img.attrs else -1)
            if(w>64 or h>64):
                return img['src']