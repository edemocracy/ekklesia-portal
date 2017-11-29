def test_index(client):
    res = client.get("/")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert '<a href="http://localhost/propositions' in content
    