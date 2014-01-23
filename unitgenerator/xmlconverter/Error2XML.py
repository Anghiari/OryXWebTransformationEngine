import xml.etree.ElementTree as ET
from constants import Constants as const

class Error2XML():
        
    def generateXML(self, url, urlOK, msg):
        
        oryx = ET.Element(const.XML_ROOT)
         
        urlnode = ET.SubElement(oryx, const.INIT_XML_URL)
        urlStatus = ET.SubElement(oryx, const.INIT_XML_URL_STATUS)
        message = ET.SubElement(oryx, const.XML_MESSAGE)
        
        urlnode.text = url
        urlStatus.text = str(urlOK)
        message.text = msg
        
        tree = ET.ElementTree(oryx)
        return tree