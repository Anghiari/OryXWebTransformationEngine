import unittest


# from communication_adapter.contenthandler import ContentHandler
from database import CacheAdapter
from communication_adapter import WebPage

class ContentHandlerTest(unittest.TestCase):
    
    webPageUrl = 'http://apb.directionsmag.com'
    
    mobileFriendlySites = (('www.facebook.com', True),
                           ('www.shahani-w.blogspot.com', False),
                           ('www.cricinfo.com', True),
                           ('www.pytest.org', False),
                           ('www.caranddriver.com', True))
    
#     def testHasMobileSite(self):
#         for url, value in self.mobileFriendlySites:              
#             result = ContentHandler.hasMobileSite(url)                    
#             self.assertEqual(True, result)
    
#     def test(self):
#         page = CacheAdapter.retrieveWebPage('http://apb.directionsmag.com')
#         self.assertEqual(True, page)
        
    def testCacheStore(self):
        webPage = WebPage('111', self.webPageUrl)
        result = CacheAdapter.storeWebPage(webPage)
        self.assertEqual(True, result)
    
    if __name__ == "__main__":
        unittest.main()   