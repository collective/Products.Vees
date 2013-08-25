from five import grok
from Products.Vees.interfaces import IVee
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.component.hooks import getSite
from Products.Vees.interfaces import DEFAULT_TEMPLATE


@grok.subscribe(IVee, IObjectAddedEvent)
def addFoldersForEventFormsFolder(vee, event):
    """ need to add subobjects now and copy template data over. """
    site = getSite()
    if hasattr(site, '_vee_templates'):
        templates = list(site._vee_templates)
        templates.insert(0, DEFAULT_TEMPLATE)
    else:
        templates = [DEFAULT_TEMPLATE]

    vee._template = templates[vee.template_index].copy()
    template = vee._template

    for content in template['main_content_table']:
        vee.invokeFactory(
            'VeeSection', content['location'],
            title=content['section_title'], goal=content['section_goal'],
            tasks=content['section_tasks'], max_height=content['max_height'])
