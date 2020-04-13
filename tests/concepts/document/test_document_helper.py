from ekklesia_portal.concepts.document.document_helper import get_section_from_document
from . import DOCUMENT_TEXT
from munch import Munch


def test_get_section_from_document():
    document = Munch(dict(text=DOCUMENT_TEXT))
    headline, content = get_section_from_document(document, '1.1')
    assert headline == 'Section 1.1'
    lines = content.splitlines()
    assert lines[0] == 'Start 1.1'
    assert lines[-1] == 'End 1.1'

    headline, content = get_section_from_document(document, '2')
    assert headline == 'Section 2'
    lines = content.splitlines()
    assert lines[0] == 'End 2'
