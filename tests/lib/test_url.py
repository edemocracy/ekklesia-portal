from ekklesia_portal.lib.url import url_change_query

def test_url_change_query():
    assert url_change_query("http://e.com/a", key="value") == "http://e.com/a?key=value"
    assert url_change_query("http://e.com/a?key=value", key2="value2") == "http://e.com/a?key=value&key2=value2"
    assert url_change_query("http://e.com/a?key=old", key="new") == "http://e.com/a?key=new"
