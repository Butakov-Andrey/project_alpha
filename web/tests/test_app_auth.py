class TestLoginPage:
    ACCOUNT = "/auth/"

    def test_login_page(self, client, data):
        response = client.get(self.ACCOUNT)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("auth_user_email") not in response.text

    def test_login_page_invalid_tokens(self, auth_client, data):
        auth_client.cookies = {
            "access_token": data.get("invalid_access_cookie"),
            "refresh_token": data.get("invalid_refresh_cookie"),
        }
        response = auth_client.get(self.ACCOUNT)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("auth_user_email") not in response.text

    def test_login_page_no_tokens(self, auth_client, data):
        auth_client.cookies = {}
        response = auth_client.get(self.ACCOUNT)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("login") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("auth_user_email") not in response.text

    def test_login(self, auth_client, data):
        response = auth_client.post(
            self.ACCOUNT,
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
            self.ACCOUNT,
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
            self.ACCOUNT,
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
    ACCOUNT = "/auth/"

    def test_logout_page(self, auth_client, data):
        response = auth_client.get(self.ACCOUNT)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("logout") in response.text
        assert data.get("logout_mes") in response.text


class TestSignUpPage:
    SIGNUP = "/auth/signup/"

    def test_signup_page_unauth(self, client, data):
        response = client.get(self.SIGNUP)
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text

    def test_signup(self, client, data):
        response = client.post(
            self.SIGNUP,
            data={
                "email": "test@example.com",
                "password": "new_password",
            },
        )
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("home_title") in response.text
        assert "test@example.com" in response.text
        assert data.get("logout") in response.text

    def test_signup_exist_email(self, client, data):
        response = client.post(
            self.SIGNUP,
            data={
                "email": "test@example.com",
                "password": "new_password",
            },
        )
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("exist_email_mes") in response.text

    def test_signup_bad_email(self, client, data):
        response = client.post(
            self.SIGNUP,
            data={
                "email": "bad_email@1",
                "password": "new_password",
            },
        )
        assert response.status_code == 200
        assert data.get("content_type") in response.headers["content-type"]
        assert data.get("signup") in response.text
        assert data.get("email") in response.text
        assert data.get("pass") in response.text
        assert data.get("invalid_email_mes") in response.text
