from Products.CMFCore.utils import getToolByName
from zope.interface import implements
import string

from plone.memoize.instance import memoize
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import IdWidget
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import TextField
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.configuration import zconf
from Products.Archetypes.ExtensibleMetadata import ExtensibleMetadata
from Products.Vees.interfaces import IVee

try:  # New CMF
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:  # Old CMF
    from Products.CMFCore import CMFCorePermissions


#from ZODB.PersistentList import PersistentList
from AccessControl import ClassSecurityInfo

from Products.Vees.config import PROJECTNAME
from Products.Vees.config import FIELDS
from Products.Vees.config import FTYPES
from Products.Vees.config import FIELDS_LEFT
from Products.Vees.config import FIELDS_RIGHT


def num2field(n):
    return "f%s" % n


def field2num(f):
    return int(f[1:])


def field2accessor(f):
    return "get%s%s" % (string.upper(f[0]), f[1:])


schema = Schema((
    StringField(
        name='id',
        # Still actually required, but the widget will
        # supply the missing value on non-submits
        required=0,
        mode='rw',
        accessor='getId',
        mutator='setId',
        default=None,
        widget=IdWidget(
            label='Short Name',
            label_msgid='label_short_name',
            description='Should not contain spaces, underscores or mixed case.'
                        ' Short Name is part of the item\'s web address.',
            description_msgid='help_shortname',
            visible={'view': 'invisible'},
            i18n_domain='plone',
        ),
    ),
    StringField(
        name='title',
        accessor='Title',
        mode='r',
        widget=StringWidget(
           modes=(),
           visible={'view': 'invisible', 'edit': 'invisible'},
        ),
    ),
 )) + ExtensibleMetadata.schema


fieldcount = 0
for field in FIELDS:
    fieldcount += 1
    if FTYPES[fieldcount - 1] == 'string':
        schema = schema + Schema((
            StringField(
                name=num2field(fieldcount),
                required=(fieldcount == 1),
                searchable=1,
                widget=StringWidget(label=field, size=60)),
         ))
    else:
        schema = schema + Schema((
            TextField(
                name=num2field(fieldcount),
                required=(fieldcount == 1),
                searchable=1,
                storage=AnnotationStorage(migrate=True),
                validators=('isTidyHtmlWithCleanup',),
                default_output_type='text/x-html-safe',
                default_content_type=zconf.ATDocument.default_content_type,
                allowable_content_types=zconf.ATDocument.allowed_content_types,
                widget=RichWidget(label=field, cols=40, rows=10)),
         ))


class Vee(ATCTContent):
    implements(IVee)

    schema = schema

    actions = ({'id': 'view',
              'name': 'View',
              'action': 'string:${object_url}/vee_view',
              'permissions': (CMFCorePermissions.View,)
    },)

    default_view = 'vee_view'
    immediate_view = 'vee_view'
    suppl_views = ('vee_view',)
    portal_type = meta_type = "Vee"

    security = ClassSecurityInfo()

    def Title(self):
        return self.getFieldValue('f1')

    def getFields(self):
        """Return a list of fields."""
        return [num2field(i) for i in range(1, len(FIELDS) + 1)]

    def getFieldValue(self, field):
        """Return value for a named field."""
        field = self.getField(field)
        return field.get(self)

    def renderFieldValue(self, field, inlineEnabled=False):
        """Return value for a named field."""
        val = self.getFieldValue(field)
        heading = FIELDS[field2num(field) - 1]
        divid = 'archetypes-fieldname-' + field
        spanid = 'parent-fieldname-' + field
        if field == 'f1':
            divclass = 'field ArchetypesField-StringField'
            spanclass = 'kssattr-atfieldname-' + field + \
                ' kssattr-templateId-widgets/string ' + \
                'kssattr-macro-string-field-view'
        else:
            divclass = 'field ArchetypesField-TextField'
            spanclass = 'kssattr-atfieldname-' + field + \
                ' kssattr-templateId-widgets/rich ' + \
                'kssattr-macro-rich-field-view'
        if inlineEnabled:
            spanclass += ' inlineEditable'
        if field2num(field) == 1:
            return """
<h1>%s</h1>
<div id="%s" class="%s"
    style=" font-size: large; font-weight: bold;margin-bottom:2em;">
  <span id="%s" class="%s">%s</span>
</div>""" % (heading, divid, divclass, spanid, spanclass, val)
        return """
<h2>%s</h2>
<div id="%s" class="%s"
        style="margin-bottom:2em;">
    <span id="%s" class="%s">%s</span>
</div>""" % (heading, divid, divclass, spanid, spanclass, val)

    def renderLeftSlot(self, row):
        """Get value on row."""
        try:
            return self.renderFieldValue(self.getLeftArm()[row])
        except IndexError:
            return ''

    def renderRightSlot(self, row):
        """Get value on row."""
        try:
            return self.renderFieldValue(self.getRightArm()[row])
        except IndexError:
            return ''

    def getTop(self):
        """Return top field."""
        return self.getFields()[0]

    def getRows(self):
        """Get rows in the Vee."""
        return range(0, len(max(self.getLeftArm(), self.getRightArm())))

    def getNumRows(self):
        """Get number of rows in the Vee."""
        return len(self.getRows())

    def getLeftArm(self):
        """Return left arm fields."""
        lowerfields = self.getFields()[1:]
        return lowerfields[:FIELDS_LEFT]

    def getRightArm(self):
        """Return right arm fields."""
        lowerfields = self.getFields()[1:]
        return lowerfields[-FIELDS_RIGHT:]

    def getBottom(self):
        """Return bottom field."""
        lowerfields = self.getFields()[1:]
        return lowerfields[FIELDS_LEFT:-FIELDS_RIGHT]

registerType(Vee, PROJECTNAME)
