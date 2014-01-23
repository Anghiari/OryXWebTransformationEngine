from unitgenerator.utilities.PageContentTypes import Text2ContentMapper, Text2ContentMapper2, HTMLSeperators,\
    TextOrderingElements, TextFormatterMap, ElementToXMLMapper
from transformengine.templategenerator.structures import BlogArticle
from urlparse import urljoin

class DataFormator():

    data = None
    soup = None
    url = None
    #nonTextTags = ["img","a"]

    def __init__(self, url, content):
#         self.data = content
#         self.soup = BeautifulSoup(self.data)
        self.soup = content
        self.url = url

    #===========================================================================
    # getFormattedData
    # Builds a BlogArticle object by extracting specific data from HTML elements
    # in the extracted article content. Uses several maps to figure out which 
    # attribute to extract.
    # @return: A BlogArticle object
    #===========================================================================    
    def getFormattedData(self):
        
        article = BlogArticle()
        lastEle = None
        lastText = None
#         inADiv = False
        for child in self.soup.recursiveChildGenerator():
            name = getattr(child, "name", None)
            innerText = child.string
            
            if(innerText and lastText and innerText == lastText):
                continue
            
            if name is not None:
                if(name in HTMLSeperators and not lastEle in HTMLSeperators):
#                     if(inADiv):
#                         article.addContent("/div", "", "")
                    article.addContent("div", "", "")
#                     inADiv = True
                elif(name in TextOrderingElements):
                    article.addContent("li", "", "")
                elif(name in TextFormatterMap and innerText):
                    if((lastEle == 'a' or lastEle in TextFormatterMap) and lastText == innerText):
                        lastEle = name
                        continue
                    article.addContent(str(name), "", innerText)
                    lastText = innerText
                elif(Text2ContentMapper.has_key(name)):
                    if(name == 'a'):
                        if(not innerText):
                            lastEle = name
                            continue
                        else:
                            lastText = innerText
                    self.getNonTextData(self.url, child, article)                        
#                 lastEle = name
            elif (innerText and not innerText.isspace()): #if this is a non empty navigatable string
                if(lastEle == 'a' and lastText == innerText):
                    continue
                if(lastEle in TextFormatterMap and lastText == innerText):
                    continue
                article.addContent("text", "", innerText)
#                 lastEle = name
            lastEle = name
            
        return article
                
    def getNonTextData(self, url, node, barticle):
        mapattr = Text2ContentMapper[node.name]
        if mapattr == 'h':
            barticle.addContent(node.name, '', node.get_text())
        elif not mapattr is '':
#             barticle.addContent(node.name, node[mapattr], node.get_text())
            atrb = node[mapattr] if node.has_attr(mapattr) else ''
            if(node.name == 'iframe' and 'youtube' not in atrb):
                return
            if(mapattr == 'src' or mapattr == 'href'):
                atrb = urljoin(url, atrb)
            barticle.addContent(node.name, atrb, node.get_text())
        
        else:
            barticle.addContent(node.name, "", "")
                   