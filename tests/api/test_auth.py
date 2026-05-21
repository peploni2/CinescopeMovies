import pytest
from models.base_models import RegisterUserResponse

class TestAuthAPI:

    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.slow
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = RegisterUserResponse(**response.json())

        # Проверки
        assert response_data.email == test_user.email, "Email не совпадает"

    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    def test_register_and_login_user(self, api_manager, registered_user, test_user):
        login_data = {
            "email": registered_user["email"],
            "password": test_user.password
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"