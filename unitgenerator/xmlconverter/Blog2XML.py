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
        
    def generateXML(self, statuscode, extractionOk, blogtitle='', favicon='', mobileurl=''):
        
        oryx=ET.Element(const.XML_ROOT)
         
        http=ET.SubElement(oryx,const.XML_HTTP)
        code=ET.SubElement(http,const.XML_CODE)
        code.text=str(statuscode)
         
        #A error message should be printed here - to do
        message=ET.SubElement(http,const.XML_MESSAGE)
        if(statuscode == const.HAS_MOBILE_SITE):
            message.text = mobileurl
        else:
            message.text=const.messages.get(statuscode, 'Unkonwn Error Code!')
        
        tree = ET.ElementTree(oryx)
        
        if(statuscode==const.HTTP_OK):
            info = ET.SubElement(oryx,const.XML_INFO)
            homepage = ET.SubElement(info, const.XML_HOMEPAGE)
            homepage.text = str(0)
            fav = ET.SubElement(info,const.XML_FAVICON)
            fav.text = favicon
            pagetitle = ET.SubElement(info, const.XML_PAGETITLE)
            pagetitle.text = blogtitle
            extraction=ET.SubElement(info,const.XML_EXTRACTION)
            extraction.text=str(extractionOk) 
            
            if(extractionOk):
                article = ET.SubElement(oryx,const.XML_ARTICLE)
                acontent = ET.SubElement(article, const.XML_CONTENT)
                
                tempParent = ET.SubElement(acontent, 'div')
                for _ in xrange(self.blogarticle.get_length()):
                    c = self.blogarticle.get_item()
                    tag = c.get_tag()
#                     lst = list(tempParent)
#                     lenth = len(lst)
                    if(tag == 'div'):
                        if(len(list(tempParent)) > 0):
                            ET.SubElement(tempParent, const.XML_ITEM)
                            tempParent = ET.SubElement(acontent, 'div')
                    else:
                        field = ET.SubElement(tempParent, const.XML_ITEM)
                        field.set("tag", c.get_tag())
                        if c.get_attr():
                            field.set("attr", Text2ContentMapper[c.get_tag()])
                            field.set("attrVal",c.get_attr())
                        field.text = c.get_text()            
                ET.SubElement(tempParent, const.XML_ITEM)
        return tree
    
    def generateTileXML(self, blogTitle, feed, extractionOk, favicon=''):
        
        oryx = ET.Element(const.XML_ROOT)
        http = ET.SubElement(oryx,const.XML_HTTP)
        code = ET.SubElement(http,const.XML_CODE)
        code.text = str(const.HTTP_OK)
        message = ET.SubElement(http,const.XML_MESSAGE)
        message.text = const.messages[const.HTTP_OK] 
        info = ET.SubElement(oryx,const.XML_INFO)
        
        extraction=ET.SubElement(info,const.XML_EXTRACTION)
        extraction.text=str(extractionOk)        
        homepage = ET.SubElement(info, const.XML_HOMEPAGE)
        homepage.text = str(1)
        pagetitle = ET.SubElement(info, const.XML_PAGETITLE)
        pagetitle.text = blogTitle
        fav = ET.SubElement(info, const.XML_FAVICON)
        fav.text = favicon
        
        
        post = ET.SubElement(oryx,const.XML_POST)
        
        for entry in feed[const.FEED_ENTRIES]:
            item = ET.SubElement(post,const.XML_ITEM)
            
            pubDate = ET.SubElement(item,const.XML_PUBLISHED)
            title = ET.SubElement(item,const.XML_TITLE)
            link = ET.SubElement(item,const.XML_LINK)
            image = ET.SubElement(item,const.XML_IMAGE)
            summary = ET.SubElement(item,const.XML_SUMMARY)
            
            pubDate.text = (entry[const.FEED_PUBLISHED])[:-6]
            title.text = entry[const.FEED_TITLE]
            link.text = entry[const.FEED_LINK]
            summary.text = self.extractTextFromHTML(entry[const.FEED_SUMMARY])
            image.text = self.extractBestImage(entry[const.FEED_SUMMARY])
            
        return ET.ElementTree(oryx)
    
    def extractTextFromHTML(self, html):
        summary = strip_tags(html)
        sumarray = summary.split()
        sumText =  ' '.join(sumarray[:60])
        if(sumText.endswith('...')):
            sumText = sumText[:-3]
        lastDot = sumText.rfind('.')
        if(lastDot > 20):
            sumText = sumText[:lastDot+1]
#         sumText = sumText.replace('Keep reading', '')
        return sumText
        
    def extractBestImage(self, html):
        soup = BeautifulSoup(html)
        imgs = soup.findAll('img')
        for img in imgs:
            w = int(re.match(r'\d+', img.attrs['width']).group() if 'width' in img.attrs else -1)
            h = int(re.match(r'\d+', img.attrs['height']).group() if 'height' in img.attrs else -1)
            if(w>64 or h>64):
                return img['src']