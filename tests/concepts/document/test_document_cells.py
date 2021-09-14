from ekklesia_portal.concepts.document.document_cells import DocumentProposeChangeCell

from . import DOCUMENT_TEXT_NUMBERED_SECTIONS


def test_document_new_draft_cell_text_with_propose_change(document, req):
    document.text = DOCUMENT_TEXT_NUMBERED_SECTIONS
    cell = DocumentProposeChangeCell(document, req)
    html = cell.text_with_propose_change
    assert 'Start' in html
    assert '{data-section}' not in html
    assert f'/p/+new_draft?document={document.id}&amp;section=1.1' in html
