import tornado
from unitgenerator.xmlconverter.Voice2XML import Voice2XML
from xml.etree  import ElementTree
import constants.Constants as const
import database.CacheAdapter as Cache
from utility_services.AuthenticateService import AuthenticateService

# session = None


'''
This class handles voice XML requests.
'''
class VoiceHandler(tornado.web.RequestHandler):
    
    mirrored_url=""
    
    
    def get(self):

        #Initial setup of cookie
        if not AuthenticateService.isVerified(self):
            #This means that the app id is not authenticated.
            self.write("This means that the app id is not authenticated.")
            
        else:
            ses_id = self.get_cookie(const.sessionID)
#             self.write("the session id is "+ses_id)
            url = self.get_argument("url", default=None, strip=False)
#             self.write("GOt URL" + url)
            if url is None:
                self.render("proxy.html") 
                return
            else:
                
                self.mirrored_url = const.HTTP_PREFIX + url
                 
                rawPage=""
                
                print("Mirrord URL:" +self.mirrored_url)
                 
                fromCache = Cache.retrieveWebPage(self.mirrored_url)
                if(fromCache is not None):
                    self.generateContent(fromCache)

          
    #===========================================================================
    # generateContent
    # Generates the voice string from the given webPage object. Uses tileXML
    # data or main article data depending on the type of the blog page.
    # @param webPage: WebPage object      
    #===========================================================================
    def generateContent(self, webPage):
        if(webPage.getVoiceXML() is not None):
            tree = webPage.getVoiceXML()
            self.sendXML(tree)
            return
        
        if(webPage.getIsHomePage() and webPage.getFeedLink()):
            if(webPage.getTileXML() is not None):
                tree = webPage.getTileXML()
#                 self.write(tree)
                tiles = ElementTree.ElementTree(ElementTree.fromstring(tree))
                vxml = Voice2XML()
                tree = vxml.generateTileVoiceXML(tiles)
                 
                webPage.setVoiceXML(ElementTree.tostring(tree.getroot(), encoding="UTF-8", method="xml"))
                Cache.storeWebPage(webPage)
                self.sendXML(ElementTree.tostring(tree.getroot(), encoding='UTF-8', method='xml'))
                return
                 
        else:
            if(webPage.getMainArticle() is not None):
#                 article = webPage.getMainArticle().encode('utf8', 'ignore')
                article = webPage.getMainArticle()
                
                vxml = Voice2XML()
                tree = vxml.generateArticleVoiceXML(article)
                 
                webPage.setVoiceXML(ElementTree.tostring(tree.getroot(), encoding="UTF-8", method="xml"))
                Cache.storeWebPage(webPage)
                 
                self.sendXML(ElementTree.tostring(tree.getroot(), encoding='UTF-8', method='xml'))
                return
    
    #===========================================================================
    # sendXML
    # Sends out a string representation of the given xml tree.
    # @param xmltree: ElementTree object 
    #===========================================================================
    def sendXML(self, xmltree):
        self.add_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'text/xml')   
        self.write(xmltree)