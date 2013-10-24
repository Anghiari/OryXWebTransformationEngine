'''
Created on May 23, 2013

@author: acer
'''

from readability.readability import Document
import urllib, urlparse
from bs4 import BeautifulSoup
import re
import feedparser

class HTMLPage:
    _html = None
    soup = None
    url = ''
    
    def __init__(self,rawPage, siteurl):
        self._html = rawPage.read()
#         print self._html
        self.soup = BeautifulSoup(self._html)
        self.url = siteurl
    
    def extract_mainarticle(self):
        readable_article = Document(self._html).summary()
        return readable_article
    
#     def extract_maintitle(self, url):
#         html = urllib.urlopen(url).read()
#         readable_title = Document(html).short_title() 
#         
#         return readable_title
    
    def getTitle(self):
        return str(self.soup.find('title').string)
    
    def getFavicon(self):
        icon_link = self.soup.find("link", rel=re.compile('.*icon.*'))
        if(icon_link is not None  and 
           icon_link.has_key('href')):
            return urlparse.urljoin(self.url, str(icon_link['href']))
        return ''
    
    def getFeedLink(self):
        head = self.soup.find('head')
        feedLink=None
            
        for feed in head.findAll("link"):
            if feed.has_key('type') and (feed["type"] == "application/rss+xml" or feed["type"] == "application/atom+xml") and feed.has_key('href') and not "/comments/" in feed['href']:
                feedLink =  feed['href']
                break
        return feedLink