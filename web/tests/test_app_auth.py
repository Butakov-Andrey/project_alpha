# TODO
class TestLoginPage:
    def test_login_page(self, client, data):
        response = client.get("/auth/")
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("auth_user_email") not in response.text

    def test_login(self, auth_client, data):
        response = auth_client.post(
            "/auth/",
            data={
                "email": data.get("auth_user_email"),
                "password": data.get("auth_user_pass"),
            },
        )
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("home_title") in response.text
        assert data.get("auth_user_email") in response.text

    def test_login_bad_email(self, auth_client, data):
        response = auth_client.post(
            "/auth/",
            data={
                "email": data.get("auth_user_email_bad"),
                "password": data.get("auth_user_pass"),
            },
        )
        assert response.status_code == 403
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("invalid_email_pass_mes") in response.text

    def test_login_bad_pass(self, auth_client, data):
        response = auth_client.post(
            "/auth/",
            data={
                "email": data.get("auth_user_email"),
                "password": data.get("auth_user_pass_bad"),
            },
        )
        assert response.status_code == 403
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("invalid_email_pass_mes") in response.text


class TestLogoutPage:
    def test_logout_page(self, auth_client, data):
        response = auth_client.get("/auth/")
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("logout") in response.text
        assert data.get("logout_mes") in response.text
