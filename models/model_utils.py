__author__ = 'ajrenold'

# Libs
import re
from unidecode import unidecode

def stormpathUserHash(user_href):
    """
        Gets user hash from stormpath user_href
    """
    return user_href[user_href.rfind('/')+1:]


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(unicode(word)).split())
    return unicode(delim.join(result))