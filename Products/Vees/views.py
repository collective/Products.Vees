from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize
from Products.Vees.interfaces import IVee
from plone.directives import dexterity
from five import grok


class OldVeeView(BrowserView):

    @memoize
    def fourone(self):
        migrationTool = getToolByName(self, 'portal_migration')
        version = migrationTool.getInstanceVersion()
        return int(version[0]) >= 3 and int(version[1]) >= 1


# Search for templates in the 'templates' directory
grok.templatedir('templates')


class VeeView(dexterity.DisplayForm):
    """The view. May will a template from content_templates/view.pt,
    and will be called 'view' unless otherwise stated.
    """
    grok.require('zope2.View')
    grok.context(IVee)
    grok.name('view')
    grok.template('veeview')

    @property
    def veetemplate(self):
        return self.context._template

    def getVeeContent(self, id):
        if id in self.context:
            return self.context[id]
        return None

    def getSectionGroup(self, group):
        results = []
        for section_id in group:
            content = self.getVeeContent(section_id)
            if not content:
                continue
            if content.hide:
                continue
            results.append(content)
        return results

    def getTopSections(self):
        return self.getSectionGroup(('top', 'top2', 'top3'))

    def getLeftSide(self):
        return self.getSectionGroup(('l6', 'l5', 'l4', 'l3', 'l2', 'l1'))

    def getRightSide(self):
        return self.getSectionGroup(('r6', 'r5', 'r4', 'r3', 'r2', 'r1'))

    def getBottom(self):
        return self.getSectionGroup(('bottom'))

    def getSectionFontSize(self, content):
        if content.id.startswith('top'):
            return self.veetemplate[content.id + '_font']
        return self.veetemplate['sections_font']
