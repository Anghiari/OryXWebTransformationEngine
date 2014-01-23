'''
Created on Jul 10, 2013

@author: acer
'''
import tornado
import constants.Constants as const
from database.DatabaseAdapter import DatabaseAdapter
from utility_services.AuthenticateService import AuthenticateService
session = None


class HomeHandler(tornado.web.RequestHandler):
    '''
        This Handler is just for the home page interface
    '''

    def get(self):
#Authentication.. This if else pattern needs to be used in each handler
        if AuthenticateService.isVerified(self):
            self.render("proxy.html")

        else:
#The authentication failed            
            self.write("No authentication ID")
    def authenticate(self, app_id):
        return self.database.isInSystem(app_id)
        
class SessionHandler(tornado.web.RequestHandler):
 
    def get(self):
        self.write("clearing this cookie :"+str(self.get_cookie(const.sessionID)))
        self.clear_cookie(const.sessionID)
        
import uuid

class Session():

        
    app_id= None
    session_id = None
    
    def __init__(self, app_id):
        self.app_id = app_id
        self.session_id = uuid.uuid4()
