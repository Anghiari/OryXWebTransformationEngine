'''
Created on Jun 20, 2013

@author: acer
'''

import tornado

import urllib2
import logging
from urllib import FancyURLopener
from contentsplitengine import HTMLPage,DataFormator
from unitgenerator.xmlconverter.Blog2XML import Blog2XML
from xml.etree  import ElementTree
import constants.Constants as const
from urlparse import urlparse, urljoin
import navigationengine.rssreader
from navigationengine import rssreader

session = None

HTTP_PREFIX = "http://"
HTTPS_PREFIX = "https://"
HAS_MOBILE_SITE = 123

class MainHandler(tornado.web.RequestHandler):
    '''
        
    '''
    
    mirrored_url=""
    
    
    def get(self):
#         print("HHHHHHHHHHHHL")
#        self.render("proxy.html")
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
                self.writeContent(rawPage)
                
    def writeContent(self, rawPage, urlFetctError = False):
        
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
                favicon = html.getFavicon()
                if(self.isHomePage(rawPage.geturl())):
                    homePage = True
                    feedlink = urljoin(rawPage.geturl(), html.getFeedLink())
                    feed = rssreader.getFeed(feedlink)
                    title = html.getTitle()
                else:
                    data=html.extract_mainarticle()
                    formator = DataFormator.DataFormator(data)
                    article=formator.getFormattedData()
                
        bxml = Blog2XML(article)
        if(homePage):
            tree = bxml.generateTileXML(title, feed, favicon)
        else:
            tree = bxml.generateXML(statuscode, favicon)
#         print ElementTree.tostring(tree.getroot())
        self.sendXML(tree)
        
    def  CheckForMobileSite(self):
        class MyOpener(FancyURLopener):
            version = 'Opera/9.80 (J2ME/MIDP; Opera Mini/9 (Compatible; MSIE:9.0; iPhone; BlackBerry9700; AppleWebKit/24.746; U; en) Presto/2.5.25 Version/10.54'

        myopener = MyOpener()
        data = myopener.open(self.mirrored_url)
        newurl = str(data.geturl())
        if(newurl.startswith("http://m.") or newurl.startswith("https://m.")):           
            bxml = Blog2XML(None)
            tree = bxml.generateXML(const.HAS_MOBILE_SITE, mobileurl=str(data.geturl()))
            self.sendXML(tree)
            return True
        return False


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
        
