import pytest
from models.base_models import CreatedFilmResponse, FilmData

class TestMoviesAPI:

    def test_create_film_with_db(self, super_admin, db_helper, film_data: FilmData):
        assert not db_helper.get_movie_by_name(film_data.name), "Фильм уже существует"

        response = super_admin.api.movies_api.create_film(film_data)
        film_id = response.json()["id"]

        assert db_helper.get_movie_by_id(film_id ), "Фильм не найден"

        super_admin.api.movies_api.delete_film(film_id )

        assert not db_helper.get_movie_by_id(film_id ), "Фильм не удален"

    def test_delete_movie_with_db(self, super_admin, db_helper, film_data: FilmData):
        movie_id = 57
        if not db_helper.get_movie_by_id(movie_id):
            db_helper.create_test_movie({"id": movie_id, **db_helper.api_movie_to_db(film_data)})

        super_admin.api.movies_api.delete_film(movie_id)

        super_admin.api.movies_api.get_film(movie_id, expected_status=404)


    @pytest.mark.slow
    def test_create_film(self, db_helper, create_test_film, film_data):
        response_data = create_test_film
        response_validate = CreatedFilmResponse(**response_data).model_dump()

        assert response_validate["name"] == film_data.name, "Имя не совпадает"
        assert response_validate["price"] == film_data.price, "Цена не совпадает"
        assert response_validate["description"] == film_data.description, "Описание не совпадает"
        assert response_validate["location"] == film_data.location, "Город не совпадает"
        assert response_validate["published"] == film_data.published, "Тип публикации не совпадает"
        assert response_validate["genreId"] == film_data.genreId, "Жанр не совпадает"

    def test_get_film_id(self, super_admin, create_test_film, film_data):
        film_id = create_test_film["id"]
        response = super_admin.api.movies_api.get_film(film_id)
        response_data = response.json()

        assert response_data["name"] == film_data.name, "Имя не совпадает"
        assert response_data["price"] == film_data.price, "Цена не совпадает"
        assert response_data["description"] == film_data.description, "Описание не совпадает"
        assert response_data["location"] == film_data.location, "Город не совпадает"
        assert response_data["published"] == film_data.published, "Тип публикации не совпадает"
        assert response_data["genreId"] == film_data.genreId, "Жанр не совпадает"

    @pytest.mark.slow
    def test_delete_film(self, super_admin, film_data):
        create_film_response = super_admin.api.movies_api.create_film(film_data)
        film_id = create_film_response.json() ["id"]
        super_admin.api.movies_api.delete_film(film_id)
        """Желательно кинуть GET, чтобы проверить что фильм точно не создался"""

    def test_patch_film(self, super_admin, create_test_film, new_film_data):
        film_id = create_test_film["id"]
        response = super_admin.api.movies_api.patch_film(new_film_data, film_id)
        response_data = response.json()

        assert response_data["name"] == new_film_data["name"], "Название фильма не совпадает"
        assert response_data["price"] == new_film_data["price"], "Цена не совпадает"
        assert response_data["description"] == new_film_data["description"], "Описание не совпадает"
        assert response_data["location"] == new_film_data["location"], "Город не совпадает"
        assert response_data["published"] == new_film_data["published"], "Тип публикации не совпадает"
        assert response_data["genreId"] == new_film_data["genreId"], "ID жанра не совпадает"

    def test_get_film_query(self, super_admin, movie_params):
        response = super_admin.api.movies_api.get_films_query(movie_params)
        response_data = response.json()

        assert response_data["page"] == movie_params["page"], "Страница не совпадает"
        assert all(
            str(movie["published"]).lower() == movie_params["published"]
            for movie in response_data["movies"]
        ), "Публикация не соответствует"

class TestNegativeMovieAPI:

    # Создание фильма с некорректным полем "name"
    @pytest.mark.slow
    def test_negative_create_film(self, super_admin, invalid_film_data, expected_status = 400):
        super_admin.api.movies_api.create_film(invalid_film_data, expected_status = expected_status)

    # GET фильма с некорректным ID
    def test_negative_get_film(self, super_admin, expected_status = 404):
        super_admin.api.movies_api.get_film(film_id = 0, expected_status = expected_status)

    # Удаление фильма с некорректным ID
    def test_negative_delete_film(self, super_admin, expected_status = 404):
        super_admin.api.movies_api.delete_film(film_id = 0, expected_status = expected_status)

    # Обновление поля фильма "name" на некорректное значение
    def test_negative_patch_film(self, super_admin, create_test_film, invalid_film_data, expected_status = 400):
        film_id = create_test_film["id"]
        super_admin.api.movies_api.patch_film(invalid_film_data, film_id, expected_status = expected_status)
        film_response = create_test_film

        assert film_response["name"] != invalid_film_data["name"], "Поле 'имя' изменилось на некорректное"

class TestUserMoviesAPI:

    @pytest.mark.slow
    def test_negative_user_create_film(self, common_user, super_admin, film_data, expected_status = 403):
        response = common_user.api.movies_api.create_film(film_data, expected_status)
        response_data = response.json()

        film_id = response_data.get("id")
        if film_id:
            super_admin.api.movies_api.delete_film(film_id)

class TestMovieWithParametrizeAndRole:

    @pytest.mark.parametrize("param", [
        {
            "minPrice": 100,
            "maxPrice": 500
        },
        {
            "location": ["SPB"]
        },
        {
            "genreId": 5
        }
    ],
    ids =[
        "цена он 100 до 500",
        "Город СПБ",
        "Жанр 5"
    ])
    def test_get_film_query_with_parametrize(self, super_admin, param):
        super_admin.api.movies_api.get_films_query(param)

    @pytest.mark.slow
    @pytest.mark.parametrize("user_fixture, expected_status",
        [
            ("super_admin", 200),
            ("admin_user", 403),
            ("common_user", 403)
        ],
        ids = ["Удаление СУПЕР АДМИНОМ", "Удаление АДМИНОМ", "Удаление ОБЫЧНЫМ ЮЗЕРОМ"])
    def test_delete_film_with_parametrize_and_user_role(self, user_fixture, super_admin, admin_user, common_user, expected_status, film_data):
        create_film_response = super_admin.api.movies_api.create_film(film_data)
        film_id = create_film_response.json()["id"]

        users = {
            "super_admin": super_admin,
            "admin_user": admin_user,
            "common_user": common_user
        }

        user = users[user_fixture]
        response = user.api.movies_api.delete_film(film_id, expected_status)

        if response.status_code != 200:
            super_admin.api.movies_api.delete_film(film_id)







