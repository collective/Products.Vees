from plone.dexterity.content import Item
from plone.dexterity.content import Container
from Products.Vees.interfaces import IVee, ISection
from zope.interface import implements
from plone.directives import dexterity
from five import grok


class Vee(Container):
    implements(IVee)


class Section(Item):
    implements(ISection)


class VeeEdit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IVee)

    def updateWidgets(self):
        super(VeeEdit, self).updateWidgets()
        self.widgets['template_index'].mode = 'hidden'
