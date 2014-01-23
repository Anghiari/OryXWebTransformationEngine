'''
Created on Jul 23, 2013

@author: acer
'''

from webclassifier.OryXdb import HostCollectionService,UrlCollectionService
from TypeCollectionService import TypeCollectionService
from TransformedCollectionService import TransformedCollectionService


#===============================================================================
# ClassifierFacade
# separate concerns between the frontend requests and data layer
#===============================================================================
class ClassifierFacade(object):


    # db services
    host_dbservice = None
    type_dbservice = None
    url_dbservice = None
    transformed_dbservice = None
    
    def __init__(self):
        self.host_dbservice = HostCollectionService()
        self.type_dbservice = TypeCollectionService()
        self.url_dbservice = UrlCollectionService()
        self.transformed_dbservice = TransformedCollectionService()
    
    #===========================================================================
    # getURLClassification
    # get the classification bruteforcingly from url collection
    #===========================================================================
    def getURLClassification(self,url):
        
        return self.url_dbservice.GetUrlClassifcation(url)
        
        
    #===========================================================================
    # getClassificationForURl
    # @return: dict a : {"provider": __, "classification": __}
    #===========================================================================
    def getClassificationForURl(self,url):
        
        a= dict()
        classification=self.host_dbservice.GetUrlClassifcation(url)
        a["provider"] = "host"
        urldoc=False
        
        if(classification is False):
            url_db=self.url_dbservice.getUrlDocument(url)
            
            if(url_db is not None):
                classification=url_db.get("classification")
                a["provider"] = "url"
                                                                  
        a["classification"]= classification
         
        #------------------------------------------------------------------------------ 
        # Connect the orange DB here
        # Require to the connect the Orange DB module here
        #------------------------------------------------------------------------------ 
           
        return a
        
     
        
    #===========================================================================
    # insertToTotalDB
    #===========================================================================
    def insertToTotalDB(self, urldoc):
        
        self.url_dbservice.insertURLToCollection(urldoc, self.url_dbservice.frontendcollection)
        self.url_dbservice.insertURLToCollection(urldoc, self.url_dbservice.frontendcollection)
    
    
        