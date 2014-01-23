'''
Created on Apr 27, 2013

@author: Anghiari
'''

import xml.etree.ElementTree as ET

def readXML(filepath):
    #'output/data/stats.xml'
    tree = ET.parse()
    root = tree.getroot(filepath)

    return root



    

            
    
            
            
            
            
            
            
            
            