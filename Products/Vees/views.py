from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize


class VeeView(BrowserView):

    @memoize
    def fourone(self):
        migrationTool = getToolByName(self, 'portal_migration')
        version = migrationTool.getInstanceVersion()
        return int(version[0]) >= 3 and int(version[1]) >= 1
