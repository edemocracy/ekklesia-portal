def test_propositions(client):
    res = client.get("/propositions")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Q1' in content
    