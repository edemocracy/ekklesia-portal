def test_argumentrelation(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1/arguments/3")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content  # proposition title
    # argument
    assert 'Ein Contra-Argument' in content  # title
    assert 'dagegen' in content  # abstract
    assert 'aus Gründen' in content  # details
