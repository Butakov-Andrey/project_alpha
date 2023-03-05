# TODO
class TestCashPage:
    def test_cash_page_auth_invalid_tokens(self, auth_client, data):
        auth_client.cookies = {
            "access_token": "bad_access_token",
            "refresh_token": "bad_refresh_token",
        }
        response = auth_client.get("/cash/")
        assert response.status_code == 401
        assert data.get("content_type") in response.headers["content-type"]
        assert "Invalid tokens!" in response.text

    def test_cash_page_auth_no_tokens(self, auth_client, data):
        auth_client.cookies = {}
        response = auth_client.get("/cash/")
        assert response.status_code == 401
        assert data.get("content_type") in response.headers["content-type"]
        assert "No tokens detected!" in response.text
