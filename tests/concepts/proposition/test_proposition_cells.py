from ekklesia_portal.concepts.proposition.proposition_cells import PropositionCell
from ekklesia_portal.datamodel import ArgumentRelation


def test_proposition_cell(proposition_with_arguments, req):
    cell = PropositionCell(proposition_with_arguments, req)
    assert cell.argument_count == 3
    assert len(cell.pro_argument_relations) == 2
    assert len(cell.contra_argument_relations) == 1
    assert isinstance(cell.pro_argument_relations[0], ArgumentRelation)
    assert isinstance(cell.contra_argument_relations[0], ArgumentRelation)


def test_proposition_share_url(proposition_with_arguments, req):
    cell = PropositionCell(proposition_with_arguments, req)
    assert req.link(proposition_with_arguments).startswith(cell.share_url)
