'''
Created on Aug 13, 2013

@author: acer
'''

import pymongo
from constants.Constants import DB_PORT, DB_URL

class TransformedCollectionService():

    client = None
    transformedcollection = None
    
    def __init__(self):
        self.client = pymongo.MongoClient(DB_URL, DB_PORT)
        self.transformedcollection = self.client.OryX.TransformedUrlCollection
        
        
    


    
    