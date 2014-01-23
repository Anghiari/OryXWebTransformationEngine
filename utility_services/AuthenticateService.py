'''
Created on May 21, 2013

@author: acer
'''

from database.DatabaseAdapter import DatabaseAdapter

class AuthenticateService(object):
    
    database = None

    def __init__(self):
        self.database = DatabaseAdapter.Instance()
#===============================================================================
# The authentication logic is implemented here
#===============================================================================
    @staticmethod
    def isVerified(handler):
        appid=handler.get_argument("app_id", default=None, strip=False)
        
#    AuthenticateService._authenticate(self, appid)
#    implement the appid verification here
#         if(appid is not None):
#             
#             return True
# 
        
#return False - Until Api_id s are hosted in DB 
        return True
    
    @staticmethod      
    def _authenticate(self, app_id):
        return self.database.isInSystem(app_id)