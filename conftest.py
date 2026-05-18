from faker import Faker
import pytest
import requests
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from enums.roles import Roles
from models.base_models import TestUser, FilmData
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helper import DBHelper

faker = Faker()

@pytest.fixture(scope = "function")
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope = "session")
def test_common_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "enums": [Roles.USER.value]
    }

@pytest.fixture(scope = "session")
def test_admin_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "enums": [Roles.ADMIN.value]
    }

@pytest.fixture(scope = "function")
def registered_user(api_manager, test_user: TestUser) -> dict:
    response = api_manager.auth_api.register_user(test_user)
    registered_user = response.json()
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
def film_data() -> FilmData:
    return FilmData(
        name = DataGenerator.generate_random_film_name(),
        imageUrl = "https://image.url",
        price = DataGenerator.generate_random_price(),
        description = DataGenerator.generate_random_description(),
        location = DataGenerator.generate_random_location(),
        published = DataGenerator.generate_random_published(),
        genreId = DataGenerator.generate_random_genre()
    )


@pytest.fixture(scope = "session")
def auth_api_manager():
    session = requests.Session()
    api_manager = ApiManager(session)
    admin_creds = ("api1@gmail.com", "asdqwe123Q")
    api_manager.auth_api.authenticate(admin_creds)
    yield api_manager
    session.close()

@pytest.fixture(scope = "function")
def create_test_film(super_admin, film_data):
    response = super_admin.api.movies_api.create_film(film_data.model_dump())
    film = response.json()
    yield film
    super_admin.api.movies_api.delete_film(film["id"])

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

@pytest.fixture(scope = "session")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope = "session")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope = "function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={
        "verified": True,
        "banned": False
    })

@pytest.fixture(scope = "session")
def creation_common_user_data(test_common_user):
    updated_data = test_common_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture(scope = "session")
def creation_admin_user_data(test_admin_user):
    updated_data = test_admin_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture(scope = "session")
def common_user(user_session, super_admin, creation_common_user_data):
    new_session = user_session()

    common_user = User(
        creation_common_user_data["email"],
        creation_common_user_data['password'],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_common_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture(scope = "session")
def creation_admin_data(creation_admin_user_data):
    updated_data = creation_admin_user_data.copy()
    updated_data.update({"enums": [Roles.ADMIN.value]})
    return updated_data

@pytest.fixture(scope = "session")
def admin_user(user_session, super_admin, creation_admin_data):
    new_session = user_session()

    admin_user = User(
        creation_admin_data["email"],
        creation_admin_data["password"],
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_admin_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "enums": [Roles.USER.value]
    }

@pytest.fixture(scope="module")
def db_session() -> Session:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope = "function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)



