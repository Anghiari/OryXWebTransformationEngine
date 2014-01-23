class WebPage:
    
    id = url = effectiveURL = htmlPage = feed = feedLink = tileXML = mainArticle = mainArticleXML = NavXML = mainXML = voiceXML = MobileSiteURL = isHomePage = extractionOk = None 
    result= None
    classification = None
    classifier = None

    
    def __init__(self, ID, url):
        self.id = ID
        self.url = url
        self.extractionOk = 1

    def get_classification(self):
        return self.__classification


    def set_classification(self, value):
        self.__classification = value


    def del_classification(self):
        del self.__classification


    def get_classifier(self):
        return self.__classifier


    def set_classifier(self, value):
        self.__classifier = value


    def del_classifier(self):
        del self.__classifier

        
    def setHtmlPage(self, html):
        self.htmlPage = html    
    def setFeed(self, feed):
        self.feed = feed    
    def setFeedLink(self, feedlink):
        self.feedLink = feedlink  
    def setTileXML(self, tileXML):
        self.tileXML = tileXML
    def setMainArticle(self, mainArticle):
        self.mainArticle = mainArticle
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
    def setVoiceXML(self, voiceXML):
        self.voiceXML = voiceXML
    def setExtractionOk(self, ok):
        self.extractionOk = ok
    def setEffectiveURL(self, effUrl):
        self.effectiveURL = effUrl
        
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
    def getMainArticle(self):
        return self.mainArticle
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
    def getVoiceXML(self):
        return self.voiceXML
    def getExtractionOk(self):
        return self.extractionOk
    def getEffectiveURL(self):
        return self.effectiveURL
    
    classifier = property(get_classifier, set_classifier, del_classifier, "classifier's docstring")
    classification = property(get_classification, set_classification, del_classification, "classification's docstring")
 
 













   