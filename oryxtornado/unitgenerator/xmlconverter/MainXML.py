from constants import Constants as const
import xml.etree.ElementTree as ET

class MainXML():

    mainelement = None
    
    def __init__(self):
        self.mainelement = ET.Element("oryx")
        
    def generateMainXML(self,  url, urlOK, hasMobileSite, hasFeed, isHome, template):
        
        oryx=ET.Element(const.XML_ROOT)
         
        urlnode=ET.SubElement(oryx, const.INIT_XML_URL)
        urlStatus=ET.SubElement(oryx, const.INIT_XML_URL_STATUS)
        mobileSite=ET.SubElement(oryx, const.INIT_XML_HAS_M_SITE)
        feedStatus=ET.SubElement(oryx, const.INIT_XML_HAS_NAV )
        pageStatus=ET.SubElement(oryx, const.INIT_XML_HOME_PAGE)
        sitetemplate=ET.SubElement(oryx,'template')
        
        urlnode.text = url
        urlStatus.text = str(urlOK)
        mobileSite.text = hasMobileSite
        feedStatus.text = str(hasFeed)
        pageStatus.text = str(isHome)
        sitetemplate.text = str(template)
        
        tree = ET.ElementTree(oryx)
        return tree
