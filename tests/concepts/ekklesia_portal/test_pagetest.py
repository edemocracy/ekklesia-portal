from ekklesia_portal.concepts.ekklesia_portal.cell.page_test import PageTestCell


def test_pagetest(client):
    res = client.get("/pagetest")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert PageTestCell.test_str in content
    assert str(PageTestCell.test_int) in content
    assert PageTestCell.test_url in content
    assert 'Hallo' in content
    assert 'Hallos' in content
