class TestClient:
    def test_client_auth(self, auth_client):
        assert "access_token" in auth_client.cookies
        assert "refresh_token" in auth_client.cookies

    def test_client_unauth(self, client):
        assert "access_token" not in client.cookies
        assert "refresh_token" not in client.cookies


class TestHomePage:
    HOME = "/"

    def test_home_page_unauth(self, client, data):
        response = client.get(self.HOME)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("home_title") in response.text
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("auth_user_email") not in response.text

    def test_home_page_auth(self, auth_client, data):
        response = auth_client.get(self.HOME)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("home_title") in response.text
        assert data.get("auth_user_email") in response.text
        assert data.get("logout") in response.text

    def test_home_page_auth_invalid_tokens(self, auth_client, data):
        auth_client.cookies = {
            "access_token": data.get("invalid_access_cookie"),
            "refresh_token": data.get("invalid_refresh_cookie"),
        }
        response = auth_client.get(self.HOME)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("home_title") in response.text
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("auth_user_email") not in response.text

    def test_home_page_auth_no_tokens(self, auth_client, data):
        auth_client.cookies = {}
        response = auth_client.get(self.HOME)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("home_title") in response.text
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("auth_user_email") not in response.text
