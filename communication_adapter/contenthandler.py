import tornado
import urllib2
from contentsplitengine import HTMLPage,DataFormator
from unitgenerator.xmlconverter.Blog2XML import Blog2XML
from xml.etree  import ElementTree
import constants.Constants as const
from urlparse import urljoin, urlparse
from navigationengine import rssreader
import database.CacheAdapter as Cache
from urllib import FancyURLopener

session = None

class ContentHandler(tornado.web.RequestHandler):
    
    mirrored_url=""
    
    
    def get(self):

        #Initial setup of cookie
        if not self.get_secure_cookie(const.sessionID):
            #This means that the app id is not authenticated. Need to pass a error xml
            self.write("This means that the app id is not authenticated. Need to pass a error xml")
            
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
                    self.writeContent(fromCache)
                else:
                    
                    try:
    #                     rawPage=urllib2.urlopen(self.mirrored_url)  
                        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36' }
                        req = urllib2.Request(self.mirrored_url, None, headers)
                        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36')
                        rawPage = urllib2.urlopen(req)
                    except Exception,e:
                        #Exception Handling Required...!!!!!!
                    #             self.response.write("An Error Occured!!\n" + str(e))
                    #             return 
    #                     logging.error('Error Fetching URL: :(:(' + str(e))
                         
                        self.write("Error Opening PAge.." + str(e))
                        return
                     
                    if(rawPage.getcode() == const.HTTP_OK):
                         if(self.CheckForMobileSite()):
                             return 
                    self.writeContentRaw(rawPage)
          
    #===========================================================================
    # writeContent
    # Extracts the main content (main article or homepage content) and sends the
    # extracted data in an XML format.
    # @param webPage: WebPage object      
    #===========================================================================
    def writeContent(self, webPage):
        if(webPage.getIsHomePage() is True):
            if(webPage.getTileXML() is not None):
                tree = webPage.getTileXML()
                self.sendXML(ElementTree.ElementTree(ElementTree.fromstring(tree)))
                return
        else:
            if(webPage.getMainArticleXML() is not None):
                tree = webPage.getMainArticleXML()
                self.sendXML(ElementTree.ElementTree(ElementTree.fromstring(tree)))
                return
        
        article = None
        homePage = False
        html = webPage.getHtmlPage()
        html.build()
        title = html.getTitle()
        favicon = html.getFavicon()
        if(webPage.getIsHomePage()):
            homePage = True
            feed = rssreader.getFeed(webPage.getFeedLink())
        else:
            data=html.extract_mainarticle()
            formator = DataFormator.DataFormator(data)
            article=formator.getFormattedData()
                
        bxml = Blog2XML(article)
        
        if(homePage):
            tree = bxml.generateTileXML(title, feed, favicon)
            webPage.setTileXML(str(tree))
        else:
            tree = bxml.generateXML(const.HTTP_OK, title, favicon)
            webPage.setMainArticleXML(ElementTree.tostring(tree.getroot(), encoding="us-ascii", method="xml"))
#         print ElementTree.tostring(tree.getroot())
#         webPage.getHtmlPage().removeSoup()
        Cache.storeWebPage(webPage)
        self.sendXML(tree)

    #===========================================================================
    # writeContentRaw
    # Given a raw html page, extracts the main content (main article or homepage 
    # content) and sends the extracted data in an XML format.
    # @param rawPage: html page from urllib
    # @param urlFetchError: if html page retrieval was unsuccessful      
    #=========================================================================== 
    def writeContentRaw(self, rawPage, urlFetctError = False):
         
        article = None
        favicon = title = ''
        homePage = False
        if(urlFetctError):
            statuscode = const.URL_FETCH_ERROR
        else:
            statuscode=rawPage.getcode()
            if(statuscode==const.HTTP_OK):
#                 print vars(rawPage)
                html = HTMLPage.HTMLPage(rawPage, rawPage.geturl())
                title = html.getTitle()
                favicon = html.getFavicon()
                if(self.isHomePage(rawPage.geturl())):
                    homePage = True
                    feedlink = urljoin(rawPage.geturl(), html.getFeedLink())
                    feed = rssreader.getFeed(feedlink)
                else:
                    data=html.extract_mainarticle()
                    formator = DataFormator.DataFormator(data)
                    article=formator.getFormattedData()
                 
        bxml = Blog2XML(article)
        if(homePage):
            tree = bxml.generateTileXML(title, feed, favicon)
        else:
            tree = bxml.generateXML(statuscode, title, favicon)
#         print ElementTree.tostring(tree.getroot())
        self.sendXML(tree)

    #===========================================================================
    # sendXML
    # Sends out a string representation of the given xml tree.
    # @param xmltree: ElementTree object 
    #===========================================================================
    def sendXML(self, xmltree):
        xmlstr = ElementTree.tostring(xmltree.getroot(), encoding='us-ascii', method='xml')
        self.add_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'text/xml')   
        self.write(xmlstr)
        
    def isHomePage(self, siteurl):
        parsedUrl = urlparse(siteurl)
        print(parsedUrl)
        size = len(parsedUrl[2])
        if(size == 0 or (size == 1 and parsedUrl[2] == '/')):
            return True
        return False
    
    def  CheckForMobileSite(self):
#         class MyOpener(FancyURLopener):
#             version = 'Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'
# 
#         myopener = MyOpener()
#         data = myopener.open(self.mirrored_url)
#         newurl = str(data.geturl())
#         if(newurl.startswith("http://m.") or newurl.startswith("https://m.")):
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
        if(newurl.startswith("http://m.") or newurl.startswith("https://m.")):
            return newurl
        return '0'