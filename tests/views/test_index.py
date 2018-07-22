def test_index(client):
    res = client.get("/")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert '<a href="http://localhost/propositions' in content

def decode_session(app, client):
    serializer = app.browser_session_interface.get_signing_serializer(app)
    return serializer.loads(client.cookies['session'])


def test_change_language(app, client):
    res = client.post("/change_language", {'lang': 'de'})
    session = decode_session(app, client)
    assert session['lang'] == 'de'

    res = client.post("/change_language", {'lang': 'fr'})
    session = decode_session(app, client)
    assert session['lang'] == 'fr'

    client.post("/change_language", {'lang': 'invalid'}, status=400)
