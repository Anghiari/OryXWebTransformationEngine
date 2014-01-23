BlogContentTypes = {
                    'TITLE': 'title', 
                    'IMAGE': 'image', 
                    'TEXT': 'text'
                    }

Text2ContentMapper = {
                      'img':'src',
                      'a':'href',
                      'h1':'h',
                      'h2':'h',
                      'iframe':'src'
                      }

Text2ContentMapper2 = {
                      'img':'src',
                      'a':'href',
                      'h1':'h',
                      'h2':'h',
                      'iframe':'src'
                      }

TextFormatterMap = {
                    'b', 'em', 'i', 'small', 'strong', 'sub', 'sup', 'ins', 'del', 'mark',
                    'code', 'kbd', 'smap', 'var', 'pre',
                    'abbr', 'address', 'bdo', 'blockquote', 'q', 'cite', 'dfn',
                    'h1', 'h2', 'h3', 'h4'
                    }

HTMLSeperators = {
                  'html', 'body', 'div', 'p', 'br', 'hr', 'nobr', 'ul', 'ol'
                  }

TextOrderingElements = {'li'}

ElementToXMLMapper = {'div':'div', 'p':'div', 'br':'div', 'hr':'div', 'nobr':'div', 'ul':'div', 'ol':'div',
                      'li':'li'
                      }