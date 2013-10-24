'''
Created on Jun 13, 2013

@author: acer
'''


import pymongo
import urlparse
from collections import deque
import json
from UrlDocuments import URLDocument

DB_URL = "192.248.8.246"
DB_PORT = 27017

class UrlCollectionService():

    client = None
    #url collection is the main repository and frontend collection is for the ui categories.
    urlcollection = None
    frontendcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.urlcollection = self.client.OryX.UrlCollection
        self.frontendcollection = self.client.OryX.FrontendCollection
        
    def getUrlCollection(self):
        return self.urlcollection
    
    def getFronendCollection(self):
        return self.frontendcollection
    
    def insertURLFromJson(self,jsonlist):
        for item in jsonlist:
            print item
            try:
                self.urlcollection.save(json.loads(item))
            except Exception,e:
                print e
        return True

    def insertURLDocument(self,urldoc):
        if(self.getUrlType(urldoc.url) is False):
            item={"url":urldoc.url,"classification":urldoc.classification, "maintag" : urldoc.maintag, "tags": urldoc.tags}
            self.urlcollection.save(item)
        else:
            print urldoc.url+" :Possible duplicate insert"
            
        
    def insertURLToCollection(self,urldoc, collection):
        if(self.getUrlType(urldoc.url) is False):
            item={"url":urldoc.url,"classification":urldoc.classification, "maintag" : urldoc.maintag, "tags": urldoc.tags}
            collection.save(item)
        else:
            print urldoc.url+" :Possible duplicate insert"
        
    def getUrlList(self,classification):
        urllist=self.urlcollection.find({"classification" : classification})
        return urllist
    
    def getUrlListFromCol(self,classification,collection):
        urllist=collection.find({"classification" : classification})
        return urllist
    
    def getUrlType(self,url):
        item=self.urlcollection.find_one({"url" : url})
        if item is None:
            return False
        return item["classification"]
    
    def getUrlTypeFromCol(self,url, collection):
        item=collection.find_one({"url" : url})
        return item["classification"]
    
    def getUrlDocument(self,url):
        item=self.urlcollection.find_one({"url" : url})
        return item    
    
    def getClassificationForURl(self,url):
        hostService = HostCollectionService()
    
        classification=hostService.GetUrlClassifcation(url)
        
        if(classification is False):
            return  self.getUrlDocument(url)
        else:
            
            urldoc= URLDocument(url,classification,"","")
        
        return urldoc

    
import urlparse

class HostCollectionService():

    client = None
    hostcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.hostcollection = self.client.OryX.HostCollection
        
    def InsertHostCollection(self,host):
        item={"domain":host.domain,"classification":host.classification, "name": host.name}
        self.hostcollection.save(item)
        
    def GetUrlClassifcation(self,url):
        url = urlparse.urlparse(url)

        urlparts = url.hostname.split('.')    

        if(urlparts != None):
            for item in urlparts:
                if(item == "www"): continue
                print(item)
                item=self.hostcollection.find_one({"domain": item})
                if(item!=None):
                    return item["classification"]
        
        return False

    def GetHost(self,url):
        url = urlparse.urlparse(url)
        subdomain = url.hostname.split('.')[1]
        hostObj= None
        if(subdomain != None):
            item=self.hostcollection.find_one({"domain": subdomain})["classification"]
            hostObj=Host(item["classification"], subdomain)
            hostObj.setName(item["name"])
            return hostObj
            
        return False
    
    
class ClassificationCollectionService():

    client = None
    classificationcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.classificationcollection = self.client.OryX.UrlTypes

    def insertNew(self,name,tags):
        item={"classification":name, "tags" : tags}
        self.classificationcollection.save(item)
        
    def getClassTypes(self):
        types=deque()
        for item in self.classificationcollection.find():
            types.append(item["classification"])
        return types

        
class Host():
    name = None
    domain = None
    classification = None
    
    def __init__(self, domain,classification, name=None):
        
        self.classification=classification
        self.domain=domain
        self.name=name
        
    def setName(self,name):
        self.name=name
        
class Category():
    name = None
    categories = None
        

    def __init__(self, domain,classification, name=None):
        self.classification=classification
        self.domain=domain
        self.name=name
