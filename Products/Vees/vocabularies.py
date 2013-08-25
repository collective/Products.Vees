from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implements
from zope.component.hooks import getSite
from Products.Vees.interfaces import DEFAULT_TEMPLATE


class TemplatesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        site = getSite()
        if hasattr(site, '_vee_templates'):
            templates = list(site._vee_templates)
            templates.insert(0, DEFAULT_TEMPLATE)
        else:
            templates = [DEFAULT_TEMPLATE]
        items = [SimpleTerm(i, i, t['title']) for i, t in
                 enumerate(templates)]
        return SimpleVocabulary(items)

TemplatesVocabularyFactory = TemplatesVocabulary()
