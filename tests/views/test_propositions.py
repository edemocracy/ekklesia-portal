def test_propositions(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Q1' in content
