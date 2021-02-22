def test_argument(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/arguments/3")
    assert 'Ein Contra-Argument' in res  # title
    assert 'dagegen' in res  # abstract
    assert 'aus Gründen' in res  # details
