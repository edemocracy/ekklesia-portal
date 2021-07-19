from morepath import redirect

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import Document
from ekklesia_portal.lib.identity import identity_manages_department, identity_manages_any_department
from ekklesia_portal.permission import CreatePermission, EditPermission

from .document_cells import DocumentCell, DocumentProposeChangeCell, DocumentsCell, EditDocumentCell, NewDocumentCell
from .document_contracts import DocumentForm
from .documents import Documents


@App.permission_rule(model=Documents, permission=CreatePermission)
def documents_create_permission(identity, model, permission):
    return identity_manages_any_department(identity)


@App.permission_rule(model=Document, permission=EditPermission)
def document_edit_permission(identity, model, permission):
    return identity_manages_department(identity, model.area.department)


@App.path(model=Documents, path='documents')
def documents():
    return Documents()


@App.path(model=Document, path='documents/{id}')
def document(request, id):
    return request.q(Document).get(id)


@App.html(model=Documents)
def index(self, request):
    cell = DocumentsCell(self, request, show_new_button=True)
    return cell.show()


@App.html(model=Documents, name='new', permission=CreatePermission)
def new(self, request):
    form = DocumentForm(request, request.link(self))
    return NewDocumentCell(request, form, form_data={}).show()


@App.html_form_post(model=Documents, form=DocumentForm, cell=NewDocumentCell, permission=CreatePermission)
def create(self, request, appstruct):
    document = Document(**appstruct)
    request.db_session.add(document)
    request.db_session.flush()
    return redirect(request.link(document))


@App.html(model=Document)
def show(self, request):
    cell = DocumentCell(self, request, show_edit_button=True, show_details=True)
    return cell.show()


@App.html(model=Document, name='edit', permission=EditPermission)
def edit(self, request):
    form = DocumentForm(request, request.link(self))
    return EditDocumentCell(self, request, form).show()


@App.html_form_post(model=Document, form=DocumentForm, cell=EditDocumentCell, permission=EditPermission)
def update(self, request, appstruct):
    self.update(**appstruct)
    return redirect(request.link(self))


@App.html(model=Document, name='propose_change')
def propose_change(self, request):
    cell = DocumentProposeChangeCell(self, request)
    return cell.show()
