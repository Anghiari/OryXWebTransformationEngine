'''
Created on Jul 23, 2013

@author: acer
'''

from webclassifier.OryXdb import HostCollectionService,UrlCollectionService
from TypeCollectionService import TypeCollectionService

class ClassifierFacade(object):
    '''
    separate concerns between the frontend requests and data layer
    '''

    host_dbservice = None
    type_dbservice = None
    url_dbservice = None
    
    def __init__(self):
        self.host_dbservice = HostCollectionService()
        self.type_dbservice = TypeCollectionService()
        self.url_dbservice = UrlCollectionService()
    
    
    def getClassification(self,url):
        
        return self.host_dbservice.GetUrlClassifcation(url)
        
        
    def getClassificationForURl(self,url):
        
        classification=self.host_dbservice.GetUrlClassifcation(url)
        
        urldoc=False
        
        if(classification is False):
            return  self.url_dbservice.getUrlDocument(url)
        else:
            
            urldoc= URLDocument(url,classification,"","")
        
        return urldoc
        
     
        
from collections import deque
        
class URLDocument():
    url = None
    classification = None
    maintag = None
    tags = None
    
    def __init__(self,url,classitype,maintagitem,tagsArray):
        self.url=url
        self.classification=classitype
        self.maintag=maintagitem
        self.tags=tagsArray
        
    
    
        