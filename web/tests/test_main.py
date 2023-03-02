import pytest


class TestMain:
    def test_create_user(self, client):
        response = client.post(
            "/auth/register/", json={"email": "test@test.com", "password": "test"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "test@test.com"
        print(data)

    @pytest.mark.asyncio
    async def test_home_page(self, async_client):
        response = await async_client.get("/")
        assert response.status_code == 200, response.text
        assert b"Homepage" in response.content
