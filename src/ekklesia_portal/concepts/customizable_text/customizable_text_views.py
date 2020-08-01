from eliot import log_call
from morepath import redirect

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import CustomizableText
from ekklesia_portal.permission import CreatePermission, EditPermission

from .customizable_text_cells import CustomizableTextCell, CustomizableTextsCell, EditCustomizableTextCell, NewCustomizableTextCell
from .customizable_text_contracts import CustomizableTextForm
from .customizable_texts import CustomizableTexts


@App.permission_rule(model=CustomizableTexts, permission=CreatePermission)
def customizable_texts_create_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.permission_rule(model=CustomizableText, permission=EditPermission)
def customizable_text_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=CustomizableTexts, path='customizable_texts')
@log_call
def customizable_texts():
    return CustomizableTexts()


@App.path(path='customizable_texts/{name}')
class CustomizableTextRedirect:

    def __init__(self, name):
        self.name = name


@App.path(model=CustomizableText, path='customizable_texts/{name}/{lang}')
@log_call
def customizable_text(request, name, lang):
    return request.q(CustomizableText).filter_by(name=name, lang=lang).scalar()


@App.html(model=CustomizableTexts, permission=CreatePermission)
@log_call
def index(self, request):
    cell = CustomizableTextsCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=CustomizableTexts, name='new', permission=CreatePermission)
@log_call
def new(self, request):
    form = CustomizableTextForm(request, request.link(self))
    return NewCustomizableTextCell(request, form, form_data={}).show()


@App.html_form_post(
    model=CustomizableTexts, form=CustomizableTextForm, cell=NewCustomizableTextCell, permission=CreatePermission
)
@log_call
def create(self, request, appstruct):
    customizable_text = CustomizableText(**appstruct)
    request.db_session.add(customizable_text)
    request.db_session.flush()
    return redirect(request.link(customizable_text))


@App.html(model=CustomizableTextRedirect)
@log_call
def customizable_text_redirect(self, request):
    lang = request.i18n.get_locale().language
    url = request.class_link(CustomizableText, {'name': self.name, 'lang': lang})
    return redirect(url)


@App.html(model=CustomizableText)
@log_call
def show(self, request):
    cell = CustomizableTextCell(self, request, show_edit_button=True, show_text=True)
    return cell.show()


@App.html(model=CustomizableText, name='edit', permission=EditPermission)
@log_call
def edit(self, request):
    form = CustomizableTextForm(request, request.link(self))
    return EditCustomizableTextCell(self, request, form).show()


@App.html_form_post(
    model=CustomizableText, form=CustomizableTextForm, cell=EditCustomizableTextCell, permission=EditPermission
)
@log_call
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
