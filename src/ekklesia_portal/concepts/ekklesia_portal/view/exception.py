from ekklesia_common.app import UnhandledRequestException
from ekklesia_portal.app import App
from ..cell.exception import ExceptionCell


@App.html(model=UnhandledRequestException)
def exception(self, request):
    return ExceptionCell(self, request).show()
