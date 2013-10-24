'''
Created on May 30, 2013

@author: acer
'''

import feedparser

def get_rssfeed(pageDoc):
    
    feed=None
            
    for rss in pageDoc.findAll("link"):
        if rss.has_key('type') and (rss["type"] == "application/rss+xml" or rss["type"] == "application/atom+xml") and rss.has_key('href') and not "/comments/" in rss['href']:
            feed = feedparser.parse(rss['href'])
            break
    return feed

def getFeed(url):
    feed = feedparser.parse(url)
    return feed
