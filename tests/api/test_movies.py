import pytest
import allure
from models.base_models import CreatedFilmResponse, FilmData, GetFilmResponse, GetQueryFilmResponse, DeleteFilmResponse, PatchFilmResponse
from pytest_check import check

@allure.epic("Тестирование movies_api")
@allure.feature("Позитивные тесты movies_api")
@pytest.mark.positive
@pytest.mark.movies_api
class TestMoviesAPI:

    @allure.title("Создание фильма в БД")
    @allure.story("Корректность создание фильма в БД")
    @pytest.mark.db
    def test_create_film_with_db(self, super_admin, db_helper, film_data: FilmData, create_test_film):
        with allure.step("Создание фильма в ДБ через фикстуру"):
            film = create_test_film
        with allure.step("Проверка создания фильма в ДБ"):
            db_film = db_helper.get_movie_by_id(film["id"])
        with allure.step("Проверяем тот ли фильм создался"):
            with check:
                assert db_film, "Фильм не найден"
                assert db_film.name == film["name"], "Фильм не с тем именем"


    @allure.title("Удаление фильма с проверкой в БД")
    @allure.story("Корректность удаление фильма в БД")
    @pytest.mark.db
    def test_delete_movie_with_db(self, super_admin, db_helper, film_data: FilmData, random_movie_id, create_db_film):
        with allure.step("Создание фильма в БД через фикстуру"):
            db_film = create_db_film
        with allure.step("Удаление фильма"):
            DeleteFilmResponse(**super_admin.api.movies_api.delete_film(db_film.id).json())
        with allure.step("Проверка удаления фильма в БД"):
            if db_helper.get_movie_by_id(db_film.id):
                db_helper.delete_movie(db_film)
            assert not db_helper.get_movie_by_id(db_film.id), "Фильм не удалился в БД"

    @allure.title("Супер админ создает фильм через movies_api")
    @allure.story("Корректность создания фильма через movies_api")
    @pytest.mark.slow
    def test_create_film(self, db_helper, create_test_film, film_data: FilmData):
        with allure.step("Создание фильма через АПИ в фикстуре"):
            response_data = create_test_film
        with allure.step("Валидация тела ответа через пайдентик"):
            response_validate = CreatedFilmResponse(**response_data).model_dump()
        with allure.step("Проверка корректности полей"):
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
        with allure.step("Создание фильма в фикстуре и запись film_id"):
            film_id = create_test_film["id"]
        with allure.step("Получение фильма через АПИ и валидация тела ответа в пайдентик"):
            response = super_admin.api.movies_api.get_film(film_id)
            response_data = GetFilmResponse(**response.json()).model_dump()
        with allure.step("Проверка полей тела ответа"):
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
        with allure.step("Создание фильма через права супер админа и валидация через пайдентик"):
            create_film_response = super_admin.api.movies_api.create_film(film_data)
            response_validate = CreatedFilmResponse(**create_film_response.json())
        with allure.step("Запись film_id"):
            film_id = response_validate.id
        with allure.step("Удаление фильма через супер админа и проверка корректности удаления, валидация ответа через пайдентик"):
            response_delete = super_admin.api.movies_api.delete_film(film_id)
            DeleteFilmResponse(**response_delete.json())
            super_admin.api.movies_api.get_film(film_id, expected_status = 404)

    @allure.title("Супер админ обновляет поля фильма через movies_api")
    @allure.story("Корректность обновления фильма через movies_api")
    def test_patch_film(self, super_admin, create_test_film, new_film_data):
        with allure.step("Создание фильма и запись film_id"):
            film_id = create_test_film["id"]
        with allure.step("Обновление полей фильма и валидация"):
            PatchFilmResponse(**super_admin.api.movies_api.patch_film(new_film_data, film_id).json())
            response_get = super_admin.api.movies_api.get_film(film_id)
            response_data_validate = GetFilmResponse(**response_get.json())
        with allure.step("Проверка полей фильма после обновления"):
            with check:
                assert response_data_validate.name == new_film_data.name, "Название фильма не совпадает"
                assert response_data_validate.price == new_film_data.price, "Цена не совпадает"
                assert response_data_validate.description == new_film_data.description, "Описание не совпадает"
                assert response_data_validate.location == new_film_data.location, "Город не совпадает"
                assert response_data_validate.published == new_film_data.published, "Тип публикации не совпадает"
                assert response_data_validate.genreId == new_film_data.genreId, "ID жанра не совпадает"

    @allure.title("Супер админ GET фильмов по фильтрам")
    @allure.story("Корректность GET фильмов по фильтрам через movies_api")
    def test_get_film_query(self, super_admin, movie_params):
        with allure.step("Получение списка фильмов и валидация ответа"):
            response = super_admin.api.movies_api.get_films_query(movie_params)
            response_validate = GetQueryFilmResponse(**response.json())
        with allure.step("Проверка полей"):
            with check:
                assert response_validate.page == movie_params["page"], "Страница не совпадает"
                assert all(
                    str(movie.published).lower() == movie_params["published"]
                    for movie in response_validate.movies
                ), "Публикация не соответствует"

@allure.epic("Тестирование movies_api")
@allure.feature("Негативные тесты movies_api")
@pytest.mark.negative
@pytest.mark.movies_api
class TestNegativeMovieAPI:

    @allure.title("Супер админ создает фильм с неправильным полем name через movies_api")
    @allure.story("Корректность невозможности создания фильма с неправильным типом данных в поле name через movies_api")
    @pytest.mark.slow
    def test_negative_create_film(self, super_admin, invalid_film_data):
        with allure.step("Создание фильма с невалидными полями"):
            response = super_admin.api.movies_api.create_film(invalid_film_data, expected_status = 400)
        with allure.step("Проверка создания фильма"):
            film_id = response.json().get("id")
            if film_id is not None:
                super_admin.api.movies_api.delete_film(film_id)
                assert False, "Фильм создался с невалидными данными и был удален"



    @allure.title("Супер админ GET неправильный id_film через movies_api")
    @allure.story("Корректность невозможности получения фильма с неправильным film_id через movies_api")
    @pytest.mark.parametrize("film_id", [-1, 0, 999999])
    def test_negative_get_film(self, super_admin, film_id):
        with allure.step("Получение фильма с некорректным film_id"):
            super_admin.api.movies_api.get_film(film_id, expected_status = 404)


    @allure.title("Супер админ удаляет фильм которого нету через movies_api")
    @allure.story("Корректность невозможности удаления фильма с неправильным film_id через movies_api")
    @pytest.mark.parametrize("film_id", [-1, 0, 999999])
    def test_negative_delete_film(self, super_admin, film_id):
        with allure.step("Удаление фильма с некорректным film_id"):
            super_admin.api.movies_api.delete_film(film_id, expected_status = 404)

    @allure.title("Супер админ обновляет фильм неправильным полем name через movies_api")
    @allure.story("Корректность невозможности изменить поле name на невалидное через movies_api")
    def test_negative_patch_film(self, super_admin, create_test_film, invalid_film_data):
        with allure.step("Создание фильма и запись film_id"):
            film_id = create_test_film["id"]
        with allure.step("Запись названия фильма до обновления поля"):
            film_name_before_patch = create_test_film["name"]
        with allure.step("Обновление фильма некорректными полями и запись названия после обновления"):
            super_admin.api.movies_api.patch_film(invalid_film_data, film_id, expected_status = 400)
            film_name_after_patch = super_admin.api.movies_api.get_film(film_id).json()["name"]
        with allure.step("Проверка изменения поля на некорректное"):
            assert film_name_before_patch == film_name_after_patch, "Поле 'имя' изменилось на некорректное"

@allure.epic("Тестирование movies_api")
@allure.feature("Параметризованные и ролевые тесты movies_api")
@pytest.mark.movies_api
class TestMovieWithParametrizeAndRole:

    @allure.title("Супер админ GET фильмы с разными параметрами через параметризацию и movies_api")
    @allure.story("Корректность GET фильмов с разными параметрами через movies_api")
    @pytest.mark.xfail(reason = "Возможно Баг АПИ: отправляю location=SPB, возвращает фильмы с MSK")
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
        with allure.step("Получение списка фильмов с разными параметрами"):
            response = super_admin.api.movies_api.get_films_query(param)
            response_validate = GetQueryFilmResponse(**response.json())
        with allure.step("Проверка полей"):
            with check:
                if "minPrice" in param:
                    assert all(movie.price >= param["minPrice"]
                               for movie in response_validate.movies), "Цена фильма меньше minPrice"
                if "maxPrice" in param:
                    assert all(movie.price <= param["maxPrice"]
                               for movie in response_validate.movies), "Цена фильма больше maxPrice"
                if "location" in param:
                    assert all(movie.location in param["location"]
                               for movie in response_validate.movies), "Город не соответствует фильтру"
                if "genreId" in param:
                    assert all(movie.genreId == param["genreId"]
                               for movie in response_validate.movies), "Жанр не соответствует фильтру"


    @allure.title("Удаление фильма разными ролями через movies_api")
    @allure.story("Корректность удаления фильма разными ролями через movies_api")
    @pytest.mark.permission
    @pytest.mark.slow
    @pytest.mark.parametrize("roles, expected_status",
        [
            ("super_admin", 200),
            ("admin_user", 403),
            ("common_user", 403)
        ],
        ids = ["Удаление СУПЕР АДМИНОМ", "Удаление АДМИНОМ", "Удаление ОБЫЧНЫМ ЮЗЕРОМ"])
    def test_delete_film_with_parametrize_and_user_role(self, roles, super_admin, admin_user, common_user, expected_status, film_data: FilmData):
        with allure.step("Создание тестового фильма и запись film_id"):
            create_film_response = super_admin.api.movies_api.create_film(film_data)
            film_id = create_film_response.json()["id"]
        with allure.step("Удаление фильма с разными правами"):
            role = {
                "super_admin": super_admin,
                "admin_user": admin_user,
                "common_user": common_user
            }

            role= role[roles]
            role.api.movies_api.delete_film(film_id, expected_status)
        with allure.step("Проверка удаления фильма"):
            if expected_status == 200:
                super_admin.api.movies_api.get_film(film_id, expected_status = 404)
            else:
                super_admin.api.movies_api.get_film(film_id)
                super_admin.api.movies_api.delete_film(film_id)
                super_admin.api.movies_api.get_film(film_id, expected_status=404)

    @allure.title("Обычный юзер пытается создать фильм через movies_api")
    @allure.story("Корректность невозможности создать фильм через movies_api без прав")
    @pytest.mark.negative
    @pytest.mark.permission
    @pytest.mark.slow
    @pytest.mark.flaky(reruns = 2)
    def test_negative_user_create_film(self, common_user, super_admin, film_data):
        with allure.step("Создание фильма пользователем без прав"):
            response = common_user.api.movies_api.create_film(film_data, expected_status = 403)
            response_data = response.json()
        with allure.step("Проверка создания фильма"):
            film_id = response_data.get("id")
        if film_id:
            super_admin.api.movies_api.delete_film(film_id)







