import tornado
import urllib2
from unitgenerator.xmlconverter.Blog2XML import Blog2XML
from xml.etree  import ElementTree
import constants.Constants as const
from urlparse import urlparse
import database.CacheAdapter as Cache
from urllib import FancyURLopener
from utility_services.AuthenticateService import AuthenticateService
from communication_adapter.ContentGenerator import ContentGenerator
from tornado.web import asynchronous
from unitgenerator.xmlconverter.Error2XML import Error2XML

# session = None


'''
This class handles content requests. Sends an XML document that is built
according to the type of the given web page (home page, inner article, etc).
'''
class ContentHandler(tornado.web.RequestHandler):
    
    mirrored_url=""
    generator = ContentGenerator()
    
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
                
#                 print("Mirrord URL:" +self.mirrored_url)
                 
                fromCache = Cache.retrieveWebPage(self.mirrored_url)
                if(fromCache is not None):
                    if(fromCache.getIsHomePage() and fromCache.getFeedLink()):
                        if(fromCache.getTileXML() is not None):
                            self.sendXML(fromCache.getTileXML())
                            return
                    else:
                        if(fromCache.getMainArticleXML() is not None):
                            self.sendXML(fromCache.getMainArticleXML())
                            return
                            
                    extractionOk= self.generator.generateContent(fromCache)
                    Cache.storeWebPage(fromCache)
                    self.sendXML(fromCache.getMainArticleXML())
                    
                else:
                    
                    try:
    #                     rawPage=urllib2.urlopen(self.mirrored_url)  
                        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36' }
                        req = urllib2.Request(self.mirrored_url, None, headers)
                        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36')
                        rawPage = urllib2.urlopen(req)
                    except Exception,e:
                        err2xml = Error2XML()
                        errTree = err2xml.generateXML(self.mirrored_url, const.URL_BAD, 'Error in fetching url!')
                        self.sendXML(ElementTree.tostring(errTree.getroot(), encoding="UTF-8", method="xml"))
                        return
                     
                    if(rawPage.getcode() == const.HTTP_OK):
                        if(self.CheckForMobileSite()):
                            return 
#                     self.generateContentRaw(rawPage)
                    isHomePage = self.isHomePage(rawPage.geturl())
                    tree = self.generator.generateContentRaw(rawPage, isHomePage)
                    self.sendXML(ElementTree.tostring(tree.getroot(), encoding="UTF-8", method="xml"))

#     def handleRequest(self, response):

    #===========================================================================
    # sendXML
    # Sends out a string representation of the given xml tree.
    # @param xmltree: ElementTree object 
    #===========================================================================
    def sendXML(self, xmltree):
        self.add_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'text/xml')   
        self.write(xmltree)
        
    def isHomePage(self, siteurl):
        parsedUrl = urlparse(siteurl)
#         print(parsedUrl)
        size = len(parsedUrl[2])
        if(size == 0 or (size == 1 and parsedUrl[2] == '/')):
            return True
        return False
    
    def CheckForMobileSite(self):
        mUrl = self.hasMobileSite()
        if(not mUrl == '0'):
            bxml = Blog2XML(None)
            tree = bxml.generateXML(const.HAS_MOBILE_SITE, mobileurl=mUrl)
            self.sendXML(tree)
            return True
        return False
    
    def hasMobileSite(self):
        class MyOpener(FancyURLopener):
            version = 'Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'

        myopener = MyOpener()
        data = myopener.open(self.mirrored_url)
        newurl = str(data.geturl())
        if(newurl.startswith("http://m.") or newurl.startswith("https://m.") or 
           newurl.startswith("http://mobi.") or newurl.startswith("https://mobi.")):
            return newurl
        return '0'