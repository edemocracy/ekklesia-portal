from munch import Munch

from ekklesia_portal.concepts.document.document_helper import get_section_from_document

from . import DOCUMENT_TEXT_MIXED_SECTION_IDS, DOCUMENT_TEXT_NUMBERED_SECTIONS


def test_get_section_from_document_numbered_sections():
    document = Munch(dict(text=DOCUMENT_TEXT_NUMBERED_SECTIONS, name='test'))
    headline, content = get_section_from_document(document, '1.1')
    assert headline == 'Section 1.1'
    lines = content.splitlines()
    assert lines[0] == 'Start 1.1'
    assert lines[-1] == 'End 1.1'

    headline, content = get_section_from_document(document, '2')
    assert headline == 'Section 2'
    lines = content.splitlines()
    assert lines[0] == 'End 2'


def test_get_section_from_document_mixed_section_ids():
    document = Munch(dict(text=DOCUMENT_TEXT_MIXED_SECTION_IDS, name='test'))
    headline, content = get_section_from_document(document, '+1.II.G.1')
    assert headline == 'SubSubSubSection'
    lines = content.splitlines()
    assert lines[0] == 'SubSubSubSection Content'
