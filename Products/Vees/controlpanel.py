from Products.Vees.interfaces import IVeeTemplate, DEFAULT_TEMPLATE
from z3c.form import form, button
from persistent.list import PersistentList
from plone.autoform.form import AutoExtensibleForm
from Products.Five import BrowserView
from plone.app.z3cform.layout import FormWrapper
from z3c.form.interfaces import NO_VALUE


class TemplateStorageProvider(object):

    @property
    def storage(self):
        store = list(self.raw_storage)
        store.insert(0, DEFAULT_TEMPLATE)
        return store

    @property
    def raw_storage(self):
        if not hasattr(self.context, '_vee_templates'):
            return PersistentList()
        return self.context._vee_templates

    def addTemplate(self, template):
        storage = self.raw_storage
        storage.append(template)
        self.context._vee_templates = storage

    def saveTemplate(self, template, index=None):
        if index is None:
            index = self.index
        storage = self.raw_storage
        storage[index - 1] = template


class VeeForm(AutoExtensibleForm, form.EditForm, TemplateStorageProvider):
    schema = IVeeTemplate

    def updateWidgets(self):
        form.EditForm.updateWidgets(self)
        mct = self.widgets['main_content_table']
        mct.allow_insert = False
        mct.allow_delete = False
        mct.auto_append = False
        mct.allow_reorder = False

    @property
    def index(self):
        return int(self.request.get('index', 'dkls').replace(
            '/@@z3cform_validate_field', ''))

    def getContent(self):
        return self.storage[self.index]

    @property
    def action(self):
        return self.request.getURL() + '?index=' + str(self.index)

    @button.buttonAndHandler(u'Save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        for key, value in data.items():
            if value == NO_VALUE:
                data[key] = None
        while True:
            if NO_VALUE in data['main_content_table']:
                data['main_content_table'].remove(NO_VALUE)
            else:
                break
        for mct in data['main_content_table']:
            for key, value in mct.items():
                if value == NO_VALUE:
                    mct[key] = None
        self.saveTemplate(data)
        return self.request.response.redirect('%s/manage-vee-templates' % (
            self.context.absolute_url()))


class VeeForm(FormWrapper):
    form = VeeForm
    label = u'Vee template'


class VeeListing(BrowserView, TemplateStorageProvider):

    label = 'Templates'
    description = ''
    status = None

    def __call__(self):

        if self.request.REQUEST_METHOD == 'POST':
            index = int(self.request.form['index'])
            if 'duplicate' in self.request.form:
                template = self.storage[index]
                self.addTemplate(template)
            elif 'delete' in self.request.form:
                del self.raw_storage[index - 1]
        return super(VeeListing, self).__call__()
