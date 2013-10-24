
class WebPage:
    
    id = url = htmlPage = feed = feedLink = tileXML = mainArticleXML = NavXML = mainXML = MobileSiteURL = isHomePage = None 
    
    
    def __init__(self, ID, url):
        self.id = ID
        self.url = url
        
    def setHtmlPage(self, html):
        self.htmlPage = html    
    def setFeed(self, feed):
        self.feed = feed    
    def setFeedLink(self, feedlink):
        self.feedLink = feedlink  
    def setTileXML(self, tileXML):
        self.tileXML = tileXML
    def setMainArticleXML(self, mainArticleXML):
        self.mainArticleXML = mainArticleXML
    def setNavXML(self, navXML):
        self.NavXML = navXML
    def setMainXML(self, mainXML):
        self.mainXML = mainXML
    def setMobileSiteURL(self, mobileUrl):
        self.MobileSiteURL = mobileUrl
    def setIsHomePage(self, homePage):
        self.isHomePage = homePage
        
    def getId(self):
        return self.id
    def getUrl(self):
        return self.url     
    def getHtmlPage(self):
        return self.htmlPage
    def getFeed(self):
        return self.feed 
    def getFeedLink(self):
        return self.feedLink 
    def getTileXML(self):
        return self.tileXML
    def getMainArticleXML(self):
        return self.mainArticleXML
    def getNavXML(self):
        return self.NavXML
    def getMainXML(self):
        return self.mainXML
    def getMobileSiteUrl(self):
        return self.MobileSiteURL
    def getIsHomePage(self):
        return self.isHomePage
 
 













   