from faker import Faker
import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager

faker = Faker()

@pytest.fixture(scope = "function")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope = "function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope = "session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope = "session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope = "function")
def film_data():
    random_film_name =  DataGenerator.generate_random_film_name()
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_random_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genre = DataGenerator.generate_random_genre()
    return {
        "name": random_film_name,
        "imageUrl": "https://image.url",
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre
    }

@pytest.fixture(scope = "session")
def auth_api_manager():
    session = requests.Session()
    api_manager = ApiManager(session)
    admin_creds = ["api1@gmail.com", "asdqwe123Q"]
    api_manager.auth_api.authenticate(admin_creds)
    yield api_manager
    session.close()

@pytest.fixture(scope = "function")
def create_test_film(auth_api_manager, film_data):
    response = auth_api_manager.movies_api.create_film(film_data)
    response_data = response.json()
    film_id = response_data["id"]
    yield film_id
    auth_api_manager.movies_api.delete_film(film_id)

@pytest.fixture(scope = "session")
def new_film_data():
    random_film_name = DataGenerator.generate_random_film_name()
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_random_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genre = DataGenerator.generate_random_genre()
    return {
        "name": random_film_name,
        "imageUrl": "https://image.url",
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre
    }

@pytest.fixture
def movie_params():
    return {
        "pageSize": DataGenerator.generate_random_page_size(),
        "page": DataGenerator.generate_random_page(),
        "minPrice": DataGenerator.generate_random_min_price(),
        "maxPrice": DataGenerator.generate_random_max_price(),
        "location": DataGenerator.generate_random_location(),
        "published": DataGenerator.generate_random_published_for_query(),
        "genreId": DataGenerator.generate_random_genre(),
        "createdAt": DataGenerator.generate_random_created_at()
    }

@pytest.fixture(scope = "function")
def invalid_film_data():
    random_film_name =  0
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_random_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genre = DataGenerator.generate_random_genre()
    return {
        "name": random_film_name,
        "imageUrl": "https://image.url",
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre
    }


