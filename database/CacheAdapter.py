import os
import redis
import cPickle
# from database.DatabaseAdapter import DatabaseAdapter


# cache = redis.Redis('localhost')

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
cache = redis.from_url(redis_url)
EXPIRE_TIME = 3600
# database = DatabaseAdapter()

def storeWebPage(webpage):
#     return database.addWebPage(webpage)
    if(webpage is not None and webpage.getUrl() is not None):
# 		print(webpage.getUrl())
        webpage.getHtmlPage().removeSoup()
        return cache.setex(webpage.getUrl(), cPickle.dumps(webpage), EXPIRE_TIME)
    return False

# def storeWebPageWithOriUrl(webpage, oriUrl):
#     if(webpage is not None and oriUrl is not None):
#         webpage.getHtmlPage().removeSoup()
#         return cache.setex(oriUrl, cPickle.dumps(webpage), EXPIRE_TIME)

def retrieveWebPage(url):
#     return database.getWebPage(url)
    if(url is None):
        return None
    webpage = cache.get(url)
    if(webpage is None):
        return None
    return cPickle.loads(webpage)
    
    return None

def delete(key):
    return cache.delete(key)
