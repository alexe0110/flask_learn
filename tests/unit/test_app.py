def test_index(client):
    response = client.get("/")
    assert response.status == "200 OK"
    assert "text/html" in response.content_type
    assert "head" in str(response.data)
    assert "footer" in str(response.data)


def test_about(client):
    response = client.get("/about")
    assert response.status == "200 OK"
    assert "text/html" in response.content_type
    assert "head" in str(response.data)
    assert "footer" in str(response.data)


def test_posts(client):
    response = client.get("/posts")
    assert response.status == "200 OK"
    assert "text/html" in response.content_type
    assert "head" in str(response.data)
    assert "footer" in str(response.data)


def test_posts_one(client):
    response = client.get("/posts/1")
    assert response.status == "200 OK"
    assert "text/html" in response.content_type
    assert "head" in str(response.data)
    assert "footer" in str(response.data)


def test_get_articles(client):
    response = client.get("/get_articles")
    assert response.status == "200 OK"
    assert response.content_type == "application/json"
