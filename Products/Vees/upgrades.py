from zope.component.hooks import getSite

_default_profile = 'profile-Products.Vees:default'


def upgrade20(context):
    site = getSite()
    pt = site.portal_types
    pt.Vee.global_allow = False
    context.runImportStepFromProfile(_default_profile, 'typeinfo')
    context.runImportStepFromProfile(_default_profile, 'workflows')
