import pytest
import allure
from models.base_models import CreatedFilmResponse, FilmData, GetFilmResponse
from pytest_check import check

@allure.epic("Тестирование movies_api")
@allure.feature("Позитивные тесты movies_api")
@pytest.mark.positive
@pytest.mark.movies_api
class TestMoviesAPI:

    @allure.title("Супер админ создает фильм напрямую в БД")
    @allure.story("Корректность создание фильма в БД")
    @pytest.mark.db
    def test_create_film_with_db(self, super_admin, db_helper, film_data: FilmData):
        assert not db_helper.get_movie_by_name(film_data.name), "Фильм уже существует"

        response = super_admin.api.movies_api.create_film(film_data)
        film_id = response.json()["id"]

        assert db_helper.get_movie_by_id(film_id ), "Фильм не найден"

        super_admin.api.movies_api.delete_film(film_id )

        assert not db_helper.get_movie_by_id(film_id ), "Фильм не удален"

    @allure.title("Супер админ удаляет фильм напрямую в БД")
    @allure.story("Корректность удаление фильма в БД")
    @pytest.mark.db
    def test_delete_movie_with_db(self, super_admin, db_helper, film_data: FilmData):
        movie_id = 57
        if not db_helper.get_movie_by_id(movie_id):
            db_helper.create_test_movie({"id": movie_id, **db_helper.api_movie_to_db(film_data)})

        super_admin.api.movies_api.delete_film(movie_id)

        super_admin.api.movies_api.get_film(movie_id, expected_status=404)

    @allure.title("Супер админ создает фильм через movies_api")
    @allure.story("Корректность создания фильма через movies_api")
    @pytest.mark.slow
    def test_create_film(self, db_helper, create_test_film, film_data: FilmData):
        response_data = create_test_film
        response_validate = CreatedFilmResponse(**response_data).model_dump()

        with check:
            assert response_validate["name"] == film_data.name, "Имя не совпадает"
            assert response_validate["price"] == film_data.price, "Цена не совпадает"
            assert response_validate["description"] == film_data.description, "Описание не совпадает"
            assert response_validate["location"] == film_data.location, "Город не совпадает"
            assert response_validate["published"] == film_data.published, "Тип публикации не совпадает"
            assert response_validate["genreId"] == film_data.genreId, "Жанр не совпадает"

    @allure.title("Супер админ GET фильм по film_id")
    @allure.story("Корректность GET фильма по film_id")
    def test_get_film_id(self, super_admin, create_test_film, film_data: FilmData):
        film_id = create_test_film["id"]
        response = super_admin.api.movies_api.get_film(film_id)
        response_data = GetFilmResponse(**response.json()).model_dump()

        with check:
            assert response_data["name"] == film_data.name, "Имя не совпадает"
            assert response_data["price"] == film_data.price, "Цена не совпадает"
            assert response_data["description"] == film_data.description, "Описание не совпадает"
            assert response_data["location"] == film_data.location, "Город не совпадает"
            assert response_data["published"] == film_data.published, "Тип публикации не совпадает"
            assert response_data["genreId"] == film_data.genreId, "Жанр не совпадает"

    @allure.title("Супер админ удаляет фильм через movies_api")
    @allure.story("Корректность удаления фильма через movies_api")
    @pytest.mark.slow
    def test_delete_film(self, super_admin, film_data: FilmData):
        create_film_response = super_admin.api.movies_api.create_film(film_data)
        film_id = create_film_response.json() ["id"]
        super_admin.api.movies_api.delete_film(film_id)
        """Желательно кинуть GET, чтобы проверить что фильм точно не создался"""

    @allure.title("Супер админ обновляет поля фильма через movies_api")
    @allure.story("Корректность обновления фильма через movies_api")
    def test_patch_film(self, super_admin, create_test_film, new_film_data):
        film_id = create_test_film["id"]
        response = super_admin.api.movies_api.patch_film(new_film_data, film_id)
        response_data = response.json()

        with check:
            assert response_data["name"] == new_film_data.name, "Название фильма не совпадает"
            assert response_data["price"] == new_film_data.price, "Цена не совпадает"
            assert response_data["description"] == new_film_data.description, "Описание не совпадает"
            assert response_data["location"] == new_film_data.location, "Город не совпадает"
            assert response_data["published"] == new_film_data.published, "Тип публикации не совпадает"
            assert response_data["genreId"] == new_film_data.genreId, "ID жанра не совпадает"

    @allure.title("Супер админ GET фильмов по фильтрам")
    @allure.story("Корректность GET фильмов по фильтрам через movies_api")
    def test_get_film_query(self, super_admin, movie_params):
        response = super_admin.api.movies_api.get_films_query(movie_params)
        response_data = response.json()

        with check:
            assert response_data["page"] == movie_params["page"], "Страница не совпадает"
            assert all(
                str(movie["published"]).lower() == movie_params["published"]
                for movie in response_data["movies"]
            ), "Публикация не соответствует"

@allure.epic("Тестирование movies_api")
@allure.feature("Негативные тесты movies_api")
@pytest.mark.negative
@pytest.mark.movies_api
class TestNegativeMovieAPI:

    @allure.title("Супер админ создает фильм с неправильным полем name через movies_api")
    @allure.story("Корректность невозможности создания фильма с неправильным типом данных в поле name через movies_api")
    @pytest.mark.slow
    def test_negative_create_film(self, super_admin, invalid_film_data, expected_status = 400):
        super_admin.api.movies_api.create_film(invalid_film_data, expected_status = expected_status)

    @allure.title("Супер админ GET неправильный id_film через movies_api")
    @allure.story("Корректность невозможности получения фильма с неправильным film_id через movies_api")
    def test_negative_get_film(self, super_admin, expected_status = 404):
        super_admin.api.movies_api.get_film(film_id = 0, expected_status = expected_status)

    @allure.title("Супер админ удаляет фильм которого нету через movies_api")
    @allure.story("Корректность невозможности удаления фильма с неправильным film_id через movies_api")
    def test_negative_delete_film(self, super_admin, expected_status = 404):
        super_admin.api.movies_api.delete_film(film_id = 0, expected_status = expected_status)

    @allure.title("Супер админ обновляет фильм неправильным полем name через movies_api")
    @allure.story("Корректность невозможности изменить поле name на невалидное через movies_api")
    def test_negative_patch_film(self, super_admin, create_test_film, invalid_film_data, expected_status = 400):
        film_id = create_test_film["id"]
        super_admin.api.movies_api.patch_film(invalid_film_data, film_id, expected_status = expected_status)
        film_response = create_test_film

        assert film_response["name"] != invalid_film_data["name"], "Поле 'имя' изменилось на некорректное"

@allure.epic("Тестирование movies_api")
@allure.feature("Параметризованные и ролевые тесты movies_api")
@pytest.mark.movies_api
class TestMovieWithParametrizeAndRole:

    @allure.title("Супер админ GET фильмы с разными параметрами через параметризацию и movies_api")
    @allure.story("Корректность GET фильмов с разными параметрами через movies_api")
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

    @allure.title("Удаление фильма разными ролями через movies_api")
    @allure.story("Корректность удаления фильма разными ролями через movies_api")
    @pytest.mark.permission
    @pytest.mark.slow
    @pytest.mark.parametrize("user_fixture, expected_status",
        [
            ("super_admin", 200),
            ("admin_user", 403),
            ("common_user", 403)
        ],
        ids = ["Удаление СУПЕР АДМИНОМ", "Удаление АДМИНОМ", "Удаление ОБЫЧНЫМ ЮЗЕРОМ"])
    def test_delete_film_with_parametrize_and_user_role(self, user_fixture, super_admin, admin_user, common_user, expected_status, film_data: FilmData):
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

    @allure.title("Обычный юзер пытается создать фильм через movies_api")
    @allure.story("Корректность невозможности создать фильм через movies_api без прав")
    @pytest.mark.negative
    @pytest.mark.permission
    @pytest.mark.slow
    def test_negative_user_create_film(self, common_user, super_admin, film_data, expected_status = 403):
        response = common_user.api.movies_api.create_film(film_data, expected_status)
        response_data = response.json()

        film_id = response_data.get("id")
        if film_id:
            super_admin.api.movies_api.delete_film(film_id)







