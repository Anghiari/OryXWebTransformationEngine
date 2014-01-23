import unittest

from contenthandler import ContentHandler
from communication_adapter.WebPage import WebPage
from database import CacheAdapter
from contentsplitengine.HTMLPage import HTMLPage
from communication_adapter.ContentGenerator import ContentGenerator
from communication_adapter.voicehandler import VoiceHandler
from communication_adapter import voicehandler
import tornado

class ComAdapterTest(unittest.TestCase):
    
    webPageUrl = 'http://apb.directionsmag.com'
    
    html = '<div><h2 style="font-size: 1.8em;margin-bottom: 0;padding-bottom: 0;"><a href="http://apb.directionsmag.com/entry/gao-report-geospatial-duplication-can-be-reduced-by-coordination/371005">GAO Report: Geospatial Duplication Can be Reduced by Coordination</a></h2></div>'
    
    mobileFriendlySites = (('www.facebook.com', True),
                           ('www.shahani-w.blogspot.com', False),
                           ('www.cricinfo.com', True),
                           ('www.pytest.org', False),
                           ('www.caranddriver.com', True))

    
    def testCacheStore(self):
        webPage = WebPage(111, self.webPageUrl)
        webPage.setHtmlPage(HTMLPage(self.html, self.webPageUrl))
        result = CacheAdapter.storeWebPage(webPage)
        self.assertEqual(True, result)
        
    def testCacheRetrieve(self):
        webPage = CacheAdapter.retrieveWebPage(self.webPageUrl)
        id = webPage.getId()
        self.assertEqual(111, id)
        

    
    if __name__ == "__main__":
        unittest.main()   