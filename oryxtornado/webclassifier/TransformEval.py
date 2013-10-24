'''
Created on Aug 14, 2013

@author: acer
'''
from communication_adapter.WebPage import WebPage
from pydoc import deque




MAX_MAIN_SCORE= 50
MAX_NAV_SCORE = 50


#===============================================================================
# TransformEval
# @attention:  This evaluation produce the result value of the WebPage object
#===============================================================================
class TransformEval():
    
    webpage= None
    criteria_list= None
    result= None

    def __init__(self, webpage):
        self.webpage=WebPage()
        self.criteria_list=deque()
        self.result=0


    def addCriteria_list(self, item):
        self.criteria_list.append(item)
        
    def evaluate(self):
            self.result +=self._evaluateMain()
            self.result += self._evaluateNav()
            self.webpage.result = self.result
            
    def _evaluateMain(self):
        res = ""
        
        if(~(self.webpage.getMainArticleXML() is None)):
            res += 50
        else: 
            res += 0
        return res
        
    def _evaluateNav(self):
        res = ""
        
        if(~(self.webpage.getNavXML() is None)):
            res += 50
        else: 
            res += 0
        
        return res
    
        
        