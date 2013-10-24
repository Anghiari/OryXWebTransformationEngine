import xml.etree.ElementTree as ET
import constants.Constants as const

class Nav2XML():
        
    def generateXML(self, statuscode, feed):
        
<<<<<<< .mine
        oryx = ET.Element("nav")
=======
        oryx=ET.Element(const.XML_NAV)
>>>>>>> .r288
        
<<<<<<< .mine
        http = ET.SubElement(oryx, "HTTP")
        code = ET.SubElement(http, "code")
        code.text = str(statuscode)
=======
        http=ET.SubElement(oryx,const.XML_HTTP)
        code=ET.SubElement(http,const.XML_CODE)
        code.text=str(statuscode)
>>>>>>> .r288
        
<<<<<<< .mine
        message = ET.SubElement(http, "message")
        message.text = const.messages.get(statuscode, 'Unkonwn Code!')
=======
        message=ET.SubElement(http, const.XML_MESSAGE)
        message.text=const.messages.get(statuscode, const.XML_UNKNOWN_CODE )
>>>>>>> .r288
        elementtree = ET.ElementTree(oryx)            
        
<<<<<<< .mine
        if(statuscode == const.HTTP_OK):
            url = ET.SubElement(http, "url")
            url.text = str(feed.url)
            tree = ET.SubElement(oryx, "tree")
            for item in feed["items"]:
                treeitem = ET.SubElement(tree, "item")
                title = ET.SubElement(treeitem, "title")
                title.text = item["title"]
                url = ET.SubElement(treeitem, "url")
                url.text = item["link"]
=======
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
>>>>>>> .r288
        
        return elementtree
        
