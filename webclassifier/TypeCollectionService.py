'''
Created on Jul 23, 2013

@author: acer
'''

import pymongo
from constants.Constants import DB_PORT, DB_URL

class TypeCollectionService():

    client = None
    hostcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.hostcollection = self.client.OryX.HostCollection
        
        
    def InsertHostCollection(self,category):
        item={"type":category.name}
        self.hostcollection.save(item)    