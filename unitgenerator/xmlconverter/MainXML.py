from constants import Constants as const
import xml.etree.ElementTree as ET

class MainXML():
        
    def generateMainXML(self, url, urlOK, effUrl, hasMobileSite, hasFeed, isHome, template, extractionOk):
        
        oryx=ET.Element(const.XML_ROOT)
         
        urlnode=ET.SubElement(oryx, const.INIT_XML_URL)
        urlStatus=ET.SubElement(oryx, const.INIT_XML_URL_STATUS)
        effectiveUrl = ET.SubElement(oryx, const.INIT_XML_EFFECTIVE_URL)
        mobileSite=ET.SubElement(oryx, const.INIT_XML_HAS_M_SITE)
        feedStatus=ET.SubElement(oryx, const.INIT_XML_HAS_NAV )
        pageStatus=ET.SubElement(oryx, const.INIT_XML_HOME_PAGE)
        sitetemplate=ET.SubElement(oryx,const.INIT_XML_TEMPLATE)
        extraction=ET.SubElement(oryx,const.XML_EXTRACTION)
        
        urlnode.text = url
        urlStatus.text = str(urlOK)
        effectiveUrl.text = effUrl
        mobileSite.text = hasMobileSite
        feedStatus.text = str(hasFeed)
        pageStatus.text = str(isHome)
        sitetemplate.text = str(template)        
        extraction.text=str(extractionOk) 
        
        tree = ET.ElementTree(oryx)
        return tree
