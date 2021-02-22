from ekklesia_portal.concepts.ekklesia_portal.cell.page_test import PageTestCell


def test_pagetest(client):
    res = client.get("/pagetest")
    html = res.html
    assert html.find(id="cell-str").text == PageTestCell.test_str
    assert html.find(id="cell-int").text == str(PageTestCell.test_int)
    a_test_url = html.find(id="cell-url").find("a")
    assert a_test_url["href"] == PageTestCell.test_url
    assert a_test_url.text == "Example.com"
    assert html.find(id="hello").text == "Hello"
    assert html.find(id="hello-plural").text == "Hellos"
