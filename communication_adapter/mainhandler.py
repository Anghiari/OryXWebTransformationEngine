import tornado

import urllib2
import logging
import functools
from urllib import FancyURLopener
from contentsplitengine import HTMLPage
from unitgenerator.xmlconverter.Blog2XML import Blog2XML
from unitgenerator.xmlconverter.MainXML import MainXML
from xml.etree  import ElementTree
import constants.Constants as const
from urlparse import urlparse
import database.CacheAdapter as Cache
from communication_adapter.WebPage import WebPage
from webclassifier.ClassfierFacade import ClassifierFacade
from utility_services.AuthenticateService import AuthenticateService
from communication_adapter.ContentGenerator import ContentGenerator
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.web import asynchronous
from unitgenerator.xmlconverter.Error2XML import Error2XML

session = None

class MainHandler(tornado.web.RequestHandler):
    '''
        
    '''
    
    mirrored_url=""
    generator = ContentGenerator()
    http_client = AsyncHTTPClient()
#     database = DatabaseAdapter.Instance()
    
    @asynchronous
    def get(self):

        mirroredUrl = ''
        #Initial setup of cookie
        if not AuthenticateService.isVerified(self):
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
                mirroredUrl = const.HTTP_PREFIX + url
                
                rawPage=""
#                 print("Mirrord URL:" +self.mirrored_url)
                
                fromCache = Cache.retrieveWebPage(mirroredUrl)
                if(fromCache is not None):
                    tree = fromCache.getMainXML()
                    self.sendXML(tree)
                    return
                
                try: 
                    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36' }
                    httpReq = HTTPRequest(mirroredUrl, 'GET', headers)
                    http_client = AsyncHTTPClient()
                    http_client.fetch(httpReq, callback=functools.partial(self.handleRequest, mirroredUrl))
                    
                except Exception,e:
                    err2xml = Error2XML()
                    errTree = err2xml.generateXML(self.mirrored_url, const.URL_BAD, 'Error in fetching url!')
                    self.sendXML(ElementTree.tostring(errTree.getroot(), encoding="UTF-8", method="xml"))
                    return
                
    def handleRequest(self, mirroredUrl, response):
        if response.error:
            err2xml = Error2XML()
            errTree = err2xml.generateXML(mirroredUrl, const.URL_BAD, str(response.error))
            self.sendXML(ElementTree.tostring(errTree.getroot(), encoding="UTF-8", method="xml"))
        else:
            self.writeMain(mirroredUrl, response)

    #===========================================================================
    # writeMain
    # Sends the initial information of the web page in an XML.
    # @param rawPage:  
    #===========================================================================
    def writeMain(self,mirroredUrl, response, urlFetchError = False):
        
        urlOK = hasMobileSite = hasFeed = isHome = ''
        rawPage = response.body
        code = response.code
#         if(not(urlFetchError or rawPage is None or not rawPage.getcode() == const.HTTP_OK)):
        if(not(urlFetchError or rawPage is None or not code == const.HTTP_OK)):
#             url = rawPage.geturl()
#             url = self.cleanUrl(url)
#             url = self.mirrored_url
            url = mirroredUrl
            effUrl = self.cleanUrl(response.effective_url)
            
            html = HTMLPage.HTMLPage(rawPage, url)
            
            webPage = WebPage(self.generateID(url), url)
            webPage.setEffectiveURL(effUrl)
            urlOK = const.URL_OK
#             hasMobileSite = self.hasMobileSite()
            #changin below line temp
            hasMobileSite = '0'
            feedLink = html.getFeedLink()
            hasFeed = 1 if(feedLink is not None) else 0
            isHome = 1 if(self.isHomePage(url)) else 0
        
            webPage.setHtmlPage(html)
            webPage.setIsHomePage(isHome)
            webPage.setFeedLink(feedLink)
            webPage.setMobileSiteURL(hasMobileSite)
#             if(feedLink is not None):
#                 webPage.setFeed(rssreader.getFeed(feedLink))
                
            
            #===================================================================
            # implementation of web classification
            #===================================================================
            classify_res= ClassifierFacade().getClassificationForURl(url)
            classification = classify_res["classification"]
            
            if classification is False:
                template = "original" 
            else:
                template = classification
            
            extractionOk  = self.generator.generateContent(webPage)
                           
            mxml = MainXML()
            tree = mxml.generateMainXML(url, urlOK, effUrl, hasMobileSite, hasFeed, isHome, template, extractionOk)
            treeXML = ElementTree.tostring(tree.getroot(), encoding="UTF-8", method="xml")
            
            webPage.setMainXML(treeXML)            
            Cache.storeWebPage(webPage)
            self.sendXML(treeXML)
            
    #===========================================================================
    # CheckForMobileSite
    # Checks if current URL has a mobile web site and sends a XML with that
    # information if yes.
    #===========================================================================        
    def  CheckForMobileSite(self):
        mUrl = self.hasMobileSite()
        if(not mUrl == '0'):
            bxml = Blog2XML(None)
            tree = bxml.generateXML(const.HAS_MOBILE_SITE, mobileurl=mUrl)
            self.sendXML(ElementTree.tostring(tree.getroot(), encoding='UTF-8', method='xml'))
            return True
        return False
    
    #===========================================================================
    # hasMobileSite
    # Finds if the current URL has a mobile web site. 
    # Returns: URL if mobile site exists, else 0
    #===========================================================================      
    def hasMobileSite(self):
        class MyOpener(FancyURLopener):
            version = 'Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'

        myopener = MyOpener()
        data = myopener.open(self.mirrored_url)
        newurl = str(data.geturl())
        if(newurl.startswith("http://m.") or newurl.startswith("https://mobi.")):
            return newurl
        return '0'

    #===========================================================================
    # sendXML
    # Sends a given XML document and finishes the connection. 
    # @param xmltree: XML document
    #=========================================================================== 
    def sendXML(self, xmltree):
        self.add_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'text/xml')   
        self.write(xmltree)  
        self.finish()      
        
    #===========================================================================
    # isHomePage
    # Checks if a given web site is a Homepage or not. 
    # @param xmltree: XML document
    #===========================================================================        
    def isHomePage(self, siteurl):
        parsedUrl = urlparse(siteurl)
#         print(parsedUrl)
        size = len(parsedUrl[2])
        if(size == 0 or (size == 1 and parsedUrl[2] == '/')):
            return True
        return False
    
    def cleanUrl(self, url):
        index = url.find('?')
        if(index>-1):
            url = url[0:index]
        
        return url[:-1] if url.endswith('/') else url
            
    
    def generateID(self, url):
        return 123
        
