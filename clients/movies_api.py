from tests.constants import MOVIES_ENDPOINT, BASE_URL_MOVIES
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session = session, base_url = BASE_URL_MOVIES)

    def create_film(self, film_data, expected_status = 201):
        return self.send_request(
            method = "POST",
            endpoint = MOVIES_ENDPOINT,
            data = film_data,
            expected_status = expected_status
        )

    def get_film(self, film_id, expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{film_id}",
            expected_status=expected_status
        )

    def delete_film(self, film_id, expected_status = 200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{film_id}",
            expected_status=expected_status
        )

    def patch_film(self, new_film_data, film_id, expected_status = 200):
        return self.send_request(
            method = "PATCH",
            endpoint = f"{MOVIES_ENDPOINT}/{film_id}",
            data = new_film_data,
            expected_status = expected_status
        )

    def get_films_query(self, movie_params,expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}",
            params = movie_params,
            expected_status=expected_status
        )