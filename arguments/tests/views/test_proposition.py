def test_proposition(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content
