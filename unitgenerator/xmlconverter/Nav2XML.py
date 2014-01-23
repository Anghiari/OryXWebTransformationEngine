import xml.etree.ElementTree as ET
import constants.Constants as const

class Nav2XML():
        
    def generateXML(self,statuscode,feed):
        
        oryx=ET.Element(const.XML_NAV)
        
        http=ET.SubElement(oryx,const.XML_HTTP)
        code=ET.SubElement(http,const.XML_CODE)
        code.text=str(statuscode)
        
        message=ET.SubElement(http, const.XML_MESSAGE)
        message.text=const.messages.get(statuscode, const.XML_UNKNOWN_CODE )
        elementtree = ET.ElementTree(oryx)            
        
        if(statuscode==const.HTTP_OK):
            url=ET.SubElement(http, const.INIT_XML_URL)
            url.text=str(feed.url)
            tree = ET.SubElement(oryx, const.XML_TREE)
            for item in feed[const.FEED_ITEMS]:
                treeitem=ET.SubElement(tree, const.XML_ITEM)
                title=ET.SubElement(treeitem, const.FEED_TITLE)
                title.text = item[const.FEED_TITLE]
                url=ET.SubElement(treeitem, const.INIT_XML_URL)
                url.text = item[const.FEED_LINK]
        
        return elementtree
        