import os
import pdict
from datetime import timedelta

# @Singleton
class DatabaseAdapter():

    filename = None
    database = None
    EXPIRE = 3600 #seconds
    
    
    def __init__(self):
        curDir = os.path.dirname(__file__)
        filename = os.path.join(curDir, 'TempCache/newcache.db')
        expireDelta = timedelta(seconds = self.EXPIRE)
        self.database = pdict.PersistentDict(filename, expires=expireDelta)
    
    def isInSystem(self, app_id):
        print app_id in  self.database
        return str(app_id) in  self.database
    
    def addID(self, app_id):
        if(app_id is not None and  self.verify(app_id)):
            self.database[app_id] = 1
            return True
        return False
    
    def removeID(self, app_id):
        del  self.database[app_id]
    
    '''Rules to verify an application ID'''
    def verify(self, app_id):
        if(len(app_id) == 10):
            return True
        return False
    
    def addWebPage(self, webPage):
        if(webPage is not None and webPage.getUrl() is not None):
            webPage.getHtmlPage().removeSoup()
            self.database[webPage.getUrl()] = webPage
            return True
        return  False
    
    def getWebPage(self, url):
        if(url is not None and url in self.database):
            webPage =  self.database[url]
            if(webPage is not None):
                return (webPage)
        return None
    
        
        
