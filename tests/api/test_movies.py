
class TestMoviesAPI:
    def test_create_film(self, auth_api_manager, create_test_film, film_data):
        response_data = create_test_film

        assert response_data["name"] == film_data["name"], "Имя не совпадает"
        assert response_data["price"] == film_data["price"], "Цена не совпадает"
        assert response_data["description"] == film_data["description"], "Описание не совпадает"
        assert response_data["location"] == film_data["location"], "Город не совпадает"
        assert response_data["published"] == film_data["published"], "Тип публикации не совпадает"
        assert response_data["genreId"] == film_data["genreId"], "Жанр не совпадает"

    def test_get_film_id(self, auth_api_manager, create_test_film, film_data):
        film_id = create_test_film["id"]
        response = auth_api_manager.movies_api.get_film(film_id)
        response_data = response.json()

        assert response_data["name"] == film_data["name"], "Имя не совпадает"
        assert response_data["price"] == film_data["price"], "Цена не совпадает"
        assert response_data["description"] == film_data["description"], "Описание не совпадает"
        assert response_data["location"] == film_data["location"], "Город не совпадает"
        assert response_data["published"] == film_data["published"], "Тип публикации не совпадает"
        assert response_data["genreId"] == film_data["genreId"], "Жанр не совпадает"

    def test_delete_film(self, auth_api_manager, film_data):
        create_film_response = auth_api_manager.movies_api.create_film(film_data)
        film_id = create_film_response.json() ["id"]
        auth_api_manager.movies_api.delete_film(film_id)

    def test_patch_film(self, auth_api_manager, create_test_film, new_film_data):
        film_id = create_test_film["id"]
        response = auth_api_manager.movies_api.patch_film(new_film_data, film_id)
        response_data = response.json()

        assert response_data["name"] == new_film_data["name"], "Название фильма не совпадает"
        assert response_data["price"] == new_film_data["price"], "Цена не совпадает"
        assert response_data["description"] == new_film_data["description"], "Описание не совпадает"
        assert response_data["location"] == new_film_data["location"], "Город не совпадает"
        assert response_data["published"] == new_film_data["published"], "Тип публикации не совпадает"
        assert response_data["genreId"] == new_film_data["genreId"], "ID жанра не совпадает"

    def test_get_film_query(self, auth_api_manager, movie_params):
        response = auth_api_manager.movies_api.get_films_query(movie_params)
        response_data = response.json()

        assert response_data["page"] == movie_params["page"], "Страница не совпадает"
        assert all(
            str(movie["published"]).lower() == movie_params["published"]
            for movie in response_data["movies"]
        ), "Публикация не соответствует"

class TestNegativeMovieAPI:
    # Создание фильма с некорректным полем "name"
    def test_negative_create_film(self, auth_api_manager, invalid_film_data, expected_status = 400):
        auth_api_manager.movies_api.create_film(invalid_film_data, expected_status = expected_status)

    # GET фильма с некорректным ID
    def test_negative_get_film(self, auth_api_manager, expected_status = 404):
        auth_api_manager.movies_api.get_film(film_id = 0, expected_status = expected_status)

    # Удаление фильма с некорректным ID
    def test_negative_delete_film(self, auth_api_manager, expected_status = 404):
        auth_api_manager.movies_api.delete_film(film_id = 0, expected_status = expected_status)

    # Обновление поля фильма "name" на некорректное значение
    def test_negative_patch_film(self, auth_api_manager, create_test_film, invalid_film_data, expected_status = 400):
        film_id = create_test_film["id"]
        auth_api_manager.movies_api.patch_film(invalid_film_data, film_id, expected_status = expected_status)
        film_response = create_test_film

        assert film_response["name"] != invalid_film_data["name"], "Поле 'имя' изменилось на некорректное"



