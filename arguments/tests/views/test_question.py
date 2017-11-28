def test_index(client):
    res = client.get("/")
    assert res.body

