'''
Created on Aug 16, 2013

@author: acer
'''

from boilerpipe.extract import Extractor

if __name__ == '__main__':
    
    
    extractor = Extractor(extractor='DefaultExtractor', url="https://facebook.com")

    print extractor.getText().encode(encoding="utf8")
