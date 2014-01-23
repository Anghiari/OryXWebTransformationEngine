import unittest
from contentsplitengine.HTMLPage import HTMLPage
import BeautifulSoup
from contentsplitengine import DataFormator2


class SplitEngineTest(unittest.TestCase):
    
    webPageUrl = 'http://apb.directionsmag.com'
    
    html = '<html><head><link rel="shortcut icon" href="http://thenextweb.com/favicon.ico" type="image/x-icon" /><link rel="alternate" type="application/rss+xml" title="TNW Network All Stories RSS Feed" href="http://feeds2.feedburner.com/thenextweb" /><title>The Next Web - International technology news, business &amp; culture</title></head><body><div class="content"><p>GAO Report: Geospatial Duplication Can be Reduced by Coordination</p></div></body></html>'
    htmlPage = HTMLPage(html, webPageUrl)
    
    def testExtraction(self):
        result = self.htmlPage.extract_mainarticle()
        hasContent = 'GAO Report: Geospatial Duplication' in result
        self.assertEqual(True, hasContent)
        
    def testExtraction2(self):
        result = self.htmlPage.extractMainArticleCustom()
        hasContent = 'GAO Report' in result
        self.assertEqual(True, hasContent)
        
    def testTitle(self):
        result = self.htmlPage.getTitle()
        hasTitle = 'The Next Web' in result
        self.assertEqual(True, hasTitle)
        
    def testFavicon(self):
        result = self.htmlPage.getFavicon()
        hasFav = 'http://thenextweb.com/favicon.ico' in result
        self.assertEqual(True, hasFav)
    
    def testFeed(self):
        result = self.htmlPage.getFeedLink()
        hasFeed = 'http://feeds2.feedburner.com/thenextweb' in result
        self.assertEqual(True, hasFeed)
        
#     def testDataFormatter(self):
#         soup = BeautifulSoup(self.html)
#         formatter = DataFormator2(self.webPageUrl, soup)
#         result = formatter.getFormattedData()
#         self.assertEqual(False, result in None)
        
    
    if __name__ == "__main__":
        unittest.main()   