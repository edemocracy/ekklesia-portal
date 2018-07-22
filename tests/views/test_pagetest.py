from ekklesia_portal.views.pagetest import PageTestCell


def test_pagetest(client):
    res = client.get("/pagetest")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert PageTestCell.test_str in content
    assert str(PageTestCell.test_int) in content
    assert PageTestCell.test_url in content
