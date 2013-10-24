import pdict
import cPickle as Pickle
from database.Singleton import Singleton

@Singleton
class DatabaseAdapter():

    filename = None
    database = None
    
    def __init__(self):
        self.filename = 'cache.db'
        self.database = pdict.PersistentDict(self.filename)
    
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
            self.database[webPage.getUrl()] = webPage
            return True
        return  False
    
    def getWebPage(self, url):
        if(url is not None):
            return self.database[self.verify(url)]