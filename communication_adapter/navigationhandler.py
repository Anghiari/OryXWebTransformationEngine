'''
Created on Jul 10, 2013

@author: acer
'''
import tornado

from bs4 import BeautifulSoup
import urllib
from navigationengine import rssreader
from unitgenerator.xmlconverter.Nav2XML import Nav2XML
from xml.etree  import ElementTree
import difflib
import constants.Constants as const
from database import CacheAdapter as Cache

HTTP_PREFIX = "http://"
HTTPS_PREFIX = "https://"


class NavigationHandler(tornado.web.RequestHandler):
    '''
    Handling navigation tree generation of web pages
    '''

    mirrored_url=""
     
    def get(self):
        print "Hahahaaaaa"
#        self.render("proxy.html")
        #Initial setup of cookie
        if not self.get_secure_cookie(const.sessionID):
            #This means that the app id is not authenticated. Need to pass a error xml
            self.write("This means that the app id is not authenticated. Need to pass a error xml")
            
        else:      
            url = self.get_argument("url", default=None, strip=False)
            
            if url is None:
                self.render("proxy.html") 
                return
            else:
                self.mirrored_url = const.HTTP_PREFIX + url      
    
            rawPage=""
            
            fromCache = Cache.retrieveWebPage(self.mirrored_url)
            if(fromCache is not None):
                self.writeNavigation(fromCache)
            else:
#                 return
                try:
                    rawPage=urllib.urlopen(self.mirrored_url)  
                except Exception,e:
                    self.response.write(e)
                    return 
 
                self.writeNavigationRaw(rawPage)
        
        
    def writeNavigation(self,webPage):
        
        if(webPage.getNavXML() is not None):
            tree = webPage.getNavXML()
            self.sendXML(ElementTree.ElementTree(ElementTree.fromstring(tree)))
            return
        
        statuscode = const.HTTP_OK
        html = webPage.getHtmlPage()
        html.build()
        feed=rssreader.getFeed(webPage.getFeedLink())
        
        if(len(feed) == 0):
            statuscode = const.NO_FEED_ERROR_CODE
        
        nxml = Nav2XML()
        tree = nxml.generateXML(statuscode,feed)
        webPage.setNavXML(ElementTree.tostring(tree.getroot(), encoding="us-ascii", method="xml"))
        Cache.storeWebPage(webPage)
        self.sendXML(tree)
        
    def writeNavigationRaw(self,rawPage):
        statuscode = rawPage.getcode()
        
        pageDoc = BeautifulSoup(rawPage)
        feed=rssreader.get_rssfeed(pageDoc)
        
        if(len(feed) == 0):
            statuscode = const.NO_FEED_ERROR_CODE
        
        nxml = Nav2XML()
        tree = nxml.generateXML(statuscode,feed)
        self.sendXML(tree)

    def sendXML(self, xmltree):
        xmlstr = ElementTree.tostring(xmltree.getroot(), encoding='us-ascii', method='xml')
        self.add_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'text/xml')
        self.write(xmlstr)
            
            