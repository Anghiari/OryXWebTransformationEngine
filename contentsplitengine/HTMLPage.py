import re
import urlparse
import constants.Constants as const
from bs4 import BeautifulSoup, Comment
from externallibs.readability import Document

class HTMLPage:
    _html = None
    soup = None
    url = ''
    BAD_TEXT = {'rate', 'comment', 'Twitter','Facebook','Print','StumbleUpon','Pinterest','Google','Email','Digg','Tumblr','Reddit','LinkedIn','Like','GPlus'}
    
    def __init__(self,rawPage, siteurl):
#         self._html = rawPage.read()
        self._html = rawPage
#         print self._html
        self.soup = BeautifulSoup(self._html)
        self.url = siteurl
    

    def extract_mainarticle(self):
        readable_article = Document(self._html).summary(True)
        return readable_article
    
    #===========================================================================
    # extractMainArticleCustom
    # Extracts the main article content from the HTML document. First try to 
    # extract using the Readability library. If extraction fails, try to remove
    # clutter and uninteresting content from the HTML document and returns a
    # cleaned document that will have the main article content.
    # @return: HTML document with main article content
    #===========================================================================
    def extractMainArticleCustom(self):
        extractionOk = const.EXTRACTION_GOOD
        readable_article = self.extract_mainarticle()
        soup = BeautifulSoup(readable_article)
        
        originalSoup = BeautifulSoup(self._html)
        comments = originalSoup.findAll(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract() 
        for elem in originalSoup.findAll(['head', 'script', 'style', 'form', 'select', 'option', 'optgroup', 'button', 'noscript', 'footer']):
            elem.extract()
        for tag in originalSoup():
            del tag['style']
            
        div = soup.find(attrs = { "class" : True })
        
        ##########new edit start
        soupText = ((''.join(soup.findAll(text=True)))[0:25]).encode('utf8', 'ignore')
        
        ##########new edit end
        if(len(soupText) < 5):
#             comments = originalSoup.findAll(text=lambda text:isinstance(text, Comment))
#             for comment in comments:
#                 comment.extract() 
            oridiv = originalSoup.find('body')
            extractionOk = const.EXTRACTION_MANUAL
        elif(div is not None and soupText== (''.join(div.findAll(text=True)).encode('utf8', 'ignore'))[0:25] ): #Also edited here
            print div['class']
            c = ' '.join(div['class'])
            
    #         print'"___________________________________________________________"'
    #         print c
    #         print (div)  
            oridiv = originalSoup.find(attrs = {'class' : c})
        else:
            oridiv = soup
#         print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
#         print oridiv
        count = 0
        
        imgs = oridiv.findAll('img')
        for img in imgs:
            w = int(re.match(r'\d+', img.attrs['width']).group() if 'width' in img.attrs else 65)
            h = int(re.match(r'\d+', img.attrs['height']).group() if 'height' in img.attrs else 65)
            if(w<64 and h<64):
                img.extract()
        
        for baddiv in oridiv('div'):            
            
#             print '---------------------'
#             print 'count' + str(count)
            count+=1
        #     print baddiv.text
            texts = baddiv.findAll(text=True)
            textCount = 0
            for t in texts:
                textCount += len(t.split())
#             print 'tot words: ' + str(textCount)
            href = baddiv.findAll('a')
#             print 'href: ' + str((len(href)))
            
            if(len(soupText) < 5):
                if(textCount > 0):
#                     print ((len(href))/(float)(textCount))
                    if((len(href)/(float)(textCount)) > .4):
                        baddiv.extract()
#                         print('EXTRACTED IN ORIGINAL HTML')
                    elif(textCount < 20 and (len(href)/(float)(textCount)) > .01):
                        baddiv.extract()
#                         print('EXTRACTED IN ORIGINAL HTML WITH LESS THAN 20 WORds')
                elif(len(href)>0):
                    baddiv.extract()
#                     print('EXTRACTED IN ORIGINAL HTML WITH NO WORDS')
            elif(textCount>0):
#                 print ((len(href))/(float)(textCount))
                if(textCount < 25 and (len(href)/(float)(textCount)) > .7):    
                    baddiv.extract()
#                     print('EXTRACTED')
                elif(textCount < 10 and (len(href)/(float)(textCount)) > .4):    
                    baddiv.extract()
#                     print('EXTRACTED')
        
#         print oridiv                     
        return oridiv, extractionOk
    
    def getTitle(self):
        title = self.soup.find('title')
        return title.string if title is not None else ''
    
    def getFavicon(self):
        icon_link = self.soup.find("link", rel=re.compile('.*icon.*'))
        if(icon_link is not None  and 
           icon_link.has_key('href')):
            return urlparse.urljoin(self.url, str(icon_link['href']))
        return ''
    
    def getFeedLink(self):
        feedLink = None
        for feed in (self.soup.findAll('link')):
            if feed.has_key('type') and (feed["type"] == "application/rss+xml" or feed["type"] == "application/atom+xml") and feed.has_key('href') and not "/comments/" in feed['href']:
                feedLink =  feed['href']
                break
        return feedLink
    
    def build(self):
#         if(self.soup is None and html is not None):
        self.soup = BeautifulSoup(self._html)
            
    def removeSoup(self):
        self.soup = None