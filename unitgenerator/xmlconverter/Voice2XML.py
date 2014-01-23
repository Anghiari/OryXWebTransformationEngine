import re
import xml.etree.ElementTree as ET
import constants.Constants as const

class Voice2XML():
    
    RX = re.compile('\s+')
    
    def generateArticleVoiceXML(self, articleText):
        oryx=ET.Element(const.XML_ROOT)
        voice=ET.SubElement(oryx, const.XML_VOICE)
        voice.text = self.RX.sub(' ', self.removeNonAscii(articleText))        
        tree = ET.ElementTree(oryx)
        return tree
    
    def generateTileVoiceXML(self, tileXML):
        text = ''
        posts = tileXML.getroot().find(const.XML_POST).findall(const.XML_ITEM)
        for items in posts:
            title = self.RX.sub(' ', self.removeNonAscii(items.find(const.XML_TITLE).text))
            summary = self.RX.sub(' ', self.removeNonAscii(items.find(const.XML_SUMMARY).text))   
            if(title and summary):       
                text = text + const.XML_VOICE_TITLE + title + const.XML_VOICE_SUMMARY + summary

        text = text[2:]
        oryx=ET.Element(const.XML_ROOT)
        voice=ET.SubElement(oryx, const.XML_VOICE)
        voice.text = text
        tree = ET.ElementTree(oryx)
        return tree
    
    def removeNonAscii(self, s):
        try:
            clean =  "".join(i for i in s if ord(i)<128)
        except Exception,e:
            clean = ''
        return clean