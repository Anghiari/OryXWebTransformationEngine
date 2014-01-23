'''
Created on Aug 13, 2013

@author: acer
'''

#===============================================================================
# Testing the service functionalities
#===============================================================================

from OryXdb import UrlCollectionService
from webclassifier.ClassfierFacade import ClassifierFacade

if __name__ == '__main__':
    service =UrlCollectionService()
    
    facade= ClassifierFacade()
    
    url ="http://www.ipahan.blogspot.com"
    
    print service.getClassificationForURl(url)
    
    print facade.getClassificationForURl(url)
                                            
    