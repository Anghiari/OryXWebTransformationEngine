from contentsplitengine import HTMLPage, DataFormator2 as DataFormator
from unitgenerator.xmlconverter.Blog2XML import Blog2XML
from xml.etree  import ElementTree
import constants.Constants as const
from urlparse import urljoin
from navigationengine import rssreader

class ContentGenerator:
    
    #===========================================================================
    # generateContent
    # Generates a XML document containing the most important content from the 
    # given webPage
    # @param webPage: A Web Page object containing the HTML document.
    #===========================================================================
    def generateContent(self, webPage):
        
        article = None
        homePage = False
        html = webPage.getHtmlPage()
        html.build()
        title = html.getTitle()
        favicon = html.getFavicon()
        extractionOk = const.EXTRACTION_GOOD
        
        feedLink = webPage.getFeedLink()
        if(webPage.getIsHomePage() and feedLink):
            homePage = True
            feed = rssreader.getFeed(feedLink)
            webPage.setFeed(feed)
        else:
            data, extractionOk = html.extractMainArticleCustom()
            formator = DataFormator.DataFormator(webPage.getEffectiveURL(), data)
            article = formator.getFormattedData()      
        bxml = Blog2XML(article)
        
        if(homePage):
            tree = bxml.generateTileXML(title, feed, extractionOk, favicon)
            webPage.setTileXML(ElementTree.tostring(tree.getroot(), encoding="UTF-8", method="xml"))
        else:
            artilcleText = data.findAll(text = True)
            text = ''
            for content in artilcleText:
                text= text + content
            text = text.strip()
            webPage.setMainArticle(text)
            if(len(text) < 5):
                webPage.setExtractionOk(0)
                extractionOk = 0
            tree = bxml.generateXML(const.HTTP_OK, extractionOk, title, favicon)
            webPage.setMainArticleXML(ElementTree.tostring(tree.getroot(), encoding="UTF-8", method="xml"))            

        return extractionOk

    #===========================================================================
    # generateContentRaw
    # Given a raw html page, extracts the main content (main article or homepage 
    # content).
    # @param rawPage: html page from urllib
    # @param isHomePage: Whether the page is a home page or not.    
    #=========================================================================== 
    def generateContentRaw(self, rawPage, isHomePage):
         
        article = None
        favicon = title = ''
        homePage = False
        feed = None
        extractionOk = const.EXTRACTION_GOOD
#         if(urlFetctError):
#             statuscode = const.URL_FETCH_ERROR
#         else:
        statuscode=rawPage.getcode()
        if(statuscode==const.HTTP_OK):
#                 print vars(rawPage)
            html = HTMLPage.HTMLPage(rawPage.read(), rawPage.geturl())
            title = html.getTitle()
            favicon = html.getFavicon()
            if(isHomePage):
                homePage = True
                feedlink = html.getFeedLink()
                if(feedlink is not None):
                    feedlink = urljoin(rawPage.geturl(), feedlink)
                    feed = rssreader.getFeed(feedlink)
            if(feed is None):
                data, extractionOk = html.extractMainArticleCustom()
                formator = DataFormator.DataFormator(rawPage.geturl(), data)
                article=formator.getFormattedData()
                 
        bxml = Blog2XML(article)
        if(homePage and feed is not None):
            tree = bxml.generateTileXML(title, feed, extractionOk, favicon)
        else:
            tree = bxml.generateXML(const.HTTP_OK, extractionOk, title, favicon)
#         print ElementTree.tostring(tree.getroot())
        return tree
