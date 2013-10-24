import redis
import cPickle

cache = redis.Redis('localhost')
EXPIRE_TIME = 3600

def storeWebPage(webpage):
	if(webpage is not None and webpage.getUrl() is not None):
# 		print(webpage.getUrl())
		webpage.getHtmlPage().removeSoup()
		return cache.setex(webpage.getUrl(), cPickle.dumps(webpage), EXPIRE_TIME)
	return False

def retrieveWebPage(url):
	if(url is None):return None
	webpage = cache.get(url)
	if(webpage is None):
		return None
	return cPickle.loads(webpage)

