
class TestMoviesAPI:
    def test_create_film(self, auth_api_manager, film_data):
        response = auth_api_manager.movies_api.create_film(film_data)
        response_data = response.json()

        assert response.status_code == 201, "Фильм не создан"
        assert response_data["name"] == film_data["name"]

        film_id = response_data["id"]
        auth_api_manager.movies_api.delete_film(film_id)

    def test_get_film_id(self, auth_api_manager, create_test_film, film_data):
        film_id = create_test_film
        response = auth_api_manager.movies_api.get_film(film_id)
        response_data = response.json()

        assert response.status_code == 200, "Фильм не найден"
        assert response_data["genreId"] == film_data["genreId"], "Жанр не совпадает"

    def test_delete_film(self, auth_api_manager, film_data):
        create_film_response = auth_api_manager.movies_api.create_film(film_data)
        film_id = create_film_response.json() ["id"]
        response = auth_api_manager.movies_api.delete_film(film_id)

        assert response.status_code == 200, "Фильм не удален"

    def test_patch_film(self, auth_api_manager, create_test_film, new_film_data):
        film_id = create_test_film
        response = auth_api_manager.movies_api.patch_film(new_film_data, film_id)
        response_data = response.json()

        assert response_data["name"] == new_film_data["name"], "Название фильма не совпадает"
        assert response_data["price"] == new_film_data["price"], "Цена не совпадает"
        assert response_data["description"] == new_film_data["description"], "Описание не совпадает"
        assert response_data["location"] == new_film_data["location"], "Город не совпадает"
        assert response_data["genreId"] == new_film_data["genreId"], "ID жанра не совпадает"

    def test_get_film_query(self, auth_api_manager, movie_params):
        response = auth_api_manager.movies_api.get_films_query(movie_params)
        response_data = response.json()

        assert response_data["page"] == movie_params["page"], "Страница не совпадает"
        assert all(
            str(movie["published"]).lower() == movie_params["published"]
            for movie in response_data["movies"]
        ), "Публикация не соответствует"

    def test_negative_create_film(self, auth_api_manager, invalid_film_data, expected_status = 400):
        response = auth_api_manager.movies_api.create_film(invalid_film_data, expected_status = expected_status)

        assert response.status_code == expected_status

    def test_negative_get_film(self, auth_api_manager, expected_status = 404):
        response = auth_api_manager.movies_api.get_film(film_id = 0, expected_status = expected_status)

        assert response.status_code == expected_status, "Фильм найден c некорректным ID"

    def test_negative_delete_film(self, auth_api_manager, expected_status = 404):
        response = auth_api_manager.movies_api.delete_film(film_id = 0, expected_status = expected_status)

        assert response.status_code == expected_status, "Фильм с некорректным ID удален"

    def test_negative_patch_film(self, auth_api_manager, create_test_film, invalid_film_data, expected_status = 400):
        film_id = create_test_film
        response = auth_api_manager.movies_api.patch_film(invalid_film_data, film_id, expected_status = expected_status)

        assert response.status_code == expected_status, "Данные фильма изменены на некорректные"


