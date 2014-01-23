HTTP_PREFIX = "http://"
HTTPS_PREFIX = "https://"
HTTP_OK = 200
HTTP_NOT_FOUND = 404
HAS_MOBILE_SITE = 123
NO_FEED_ERROR_CODE = 101
URL_FETCH_ERROR = 666
EXTRACTION_GOOD = 1
EXTRACTION_MANUAL = 2
URL_OK = 1
URL_BAD = 0
messages = {200:'OK', 400: 'Bad Request', 401: 'Unauthorized', 404:'Web Page Not Found', 
            403: 'Forbidden', 500: 'Internal Server Error',
            101: 'No Feed Found', 666: 'Error Fetching URL'}

XML_ROOT = 'oryx'
INIT_XML_ID = 'id'
INIT_XML_URL = 'url'
INIT_XML_EFFECTIVE_URL = 'effUrl'
INIT_XML_URL_STATUS = 'urlStatus'
INIT_XML_HOME_PAGE = 'isHome'
INIT_XML_HAS_NAV = 'hasFeed'
INIT_XML_HAS_M_SITE = 'mobileSite'
INIT_XML_TEMPLATE = 'template'

XML_HTTP = 'HTTP'
XML_CODE = 'code'
XML_MESSAGE = 'message'
XML_EXTRACTION = 'extraction'
XML_INFO = 'info'
XML_HOMEPAGE = 'homepage'
XML_FAVICON = 'favicon'
XML_PAGETITLE = 'pagetitle'
XML_ARTICLE = 'article'
XML_CONTENT = 'content'
XML_VOICE = 'voice'
XML_ITEM = 'item'
XML_POST = 'post'
XML_PUBLISHED = 'published'
XML_TITLE = 'title'
XML_LINK = 'link'
XML_IMAGE = 'image'
XML_SUMMARY = 'summary'
XML_NAV = 'nav'
XML_UNKNOWN_CODE = 'Unkonwn Code!'
XML_TREE = 'tree'

XML_VOICE_TITLE = '. Title: '
XML_VOICE_SUMMARY = '. Summary: '

FEED_ENTRIES = 'entries'
FEED_PUBLISHED = 'published'
FEED_TITLE = 'title'
FEED_LINK = 'link'
FEED_IMAGE = 'image'
FEED_SUMMARY = 'summary'
FEED_ITEMS = 'items'

sessionID='oryx_id'

DB_URL = "192.248.15.233"
DB_PORT = 27017

#===============================================================================
# Email Service Settings
#===============================================================================

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_PWD = "anghiari"
EMAIL_SENDER = "oryxwebvisualizer@gmail.com"

    