from eliot import log_call
from morepath import redirect

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Page
from ekklesia_portal.permission import CreatePermission, EditPermission

from .page_cells import EditPageCell, NewPageCell, PageCell, PagesCell
from .page_contracts import PageForm
from .pages import Pages


@App.permission_rule(model=Pages, permission=CreatePermission)
def pages_create_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.permission_rule(model=Page, permission=EditPermission)
def page_edit_permission(identity, model, permission):
    return identity.has_global_admin_permissions


@App.path(model=Pages, path='pages')
@log_call
def pages():
    return Pages()


@App.path(path='pages/{name}')
class PageRedirect:

    def __init__(self, name):
        self.name = name


@App.path(model=Page, path='pages/{name}/{lang}')
@log_call
def page(request, name, lang):
    db_page = request.q(Page).filter_by(name=name, lang=lang).scalar()
    if db_page is None:
        use_lang = request.app.settings.app.fallback_language.lower()
        db_page = request.q(Page).filter_by(name=name, lang=use_lang).scalar()
    return db_page


@App.html(model=Pages, permission=CreatePermission)
@log_call
def index(self, request):
    cell = PagesCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=Pages, name='new', permission=CreatePermission)
@log_call
def new(self, request):
    form = PageForm(request, request.link(self))
    return NewPageCell(request, form, form_data={}).show()


# this level of abstraction is nice, but the goal is:
# @App.html_create(Page)
@App.html_form_post(model=Pages, form=PageForm, cell=NewPageCell, permission=CreatePermission)
@log_call
def create(self, request, appstruct):
    page = Page(**appstruct)
    request.db_session.add(page)
    request.db_session.flush()
    return redirect(request.link(page))


@App.html(model=PageRedirect)
@log_call
def page_redirect(self, request):
    lang = request.i18n.get_locale().language
    url = request.class_link(Page, {'name': self.name, 'lang': lang})
    return redirect(url)


@App.html(model=Page)
@log_call
def show(self, request):
    cell = PageCell(self, request, show_edit_button=True, show_text=True)
    return cell.show()


@App.html(model=Page, name='edit', permission=EditPermission)
@log_call
def edit(self, request):
    form = PageForm(request, request.link(self))
    return EditPageCell(self, request, form).show()


# this level of abstraction is nice, but the goal is:
# @App.html_update(Page)
@App.html_form_post(model=Page, form=PageForm, cell=EditPageCell, permission=EditPermission)
@log_call
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))
