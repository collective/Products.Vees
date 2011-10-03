try:
    from Products.CMFCore import CMFCorePermissions
except:
    from Products.CMFCore import permissions as CMFCorePermissions

from types import UnicodeType

ADD_PERMISSIONS = {
    'Vee': 'Products.Vees: Add Vee',
}

PROJECTNAME = "Vees"
SKINS_DIR = 'skins'
SKIN_FOLDERS = ('Vees',)
SKIN_NAME = 'Vees'

## FIELDS = ('Focus Question',
##           'Material and Methods',
##           'Raw Data',
##           'Transformation',
##           'Results',
##           'Knowledge Claim',
##           'Value Claim',
##           'Supporting Concepts',
##           'World Views')
FIELDS = ('Focus Question',
          'Background Knowledge',
          'Related Vocabulary',
          'Materials and Methods',
          'Value Claim',
          'Knowledge Claim',
          'Results',
          'Transformation',
          'Raw Data',
          )

FTYPES = ('string',
          'text',
          'text',
          'text',
          'text',
          'text',
          'text',
          'text',
          'text',
          )

FIELDS_LEFT = 2
FIELDS_BOTTOM = 1
FIELDS_RIGHT = 5

assert (1 + FIELDS_LEFT + FIELDS_RIGHT + FIELDS_BOTTOM) == len(FIELDS)
assert len(FIELDS) == len(FTYPES)

GLOBALS = globals()


def to_unicode(s, encoding='iso-8859-1'):
    us = None
    if not s:
        us = u''
    elif type(s) == UnicodeType:
        us = s
    else:
        us = unicode(s, encoding)
    return us.encode('utf-8')
