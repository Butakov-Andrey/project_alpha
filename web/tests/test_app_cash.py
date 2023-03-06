# TODO
class TestCashPage:
    CASH = "/cash/"

    def test_cash_page_auth_invalid_tokens(self, auth_client, data):
        auth_client.cookies = {
            "access_token": data.get("invalid_access_cookie"),
            "refresh_token": data.get("invalid_refresh_cookie"),
        }
        response = auth_client.get(self.CASH)
        assert response.status_code == 401
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("invalid_tokens_mes") in response.text

    def test_cash_page_auth_no_tokens(self, auth_client, data):
        auth_client.cookies = {}
        response = auth_client.get(self.CASH)
        assert response.status_code == 401
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("no_tokens_mes") in response.text

    def test_cash_page_unauth(self, client, data):
        response = client.get(self.CASH)
        assert response.status_code == 401
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("no_tokens_mes") in response.text
