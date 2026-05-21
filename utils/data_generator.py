import random
import string
from faker import Faker
import datetime
from uuid import uuid4

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6,18)
        remaining_chars = ''.join(random.choices(all_chars, k = remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_film_name():
        return f"{faker.first_name()} {faker.last_name()} {uuid4()}"

    @staticmethod
    def generate_random_price():
        return faker.random_int(min=1, max=100)

    @staticmethod
    def generate_random_int(length: int):
        return faker.random_number(
            digits = length,
            fix_len = True
        )

    @staticmethod
    def generate_random_description():
        return f"{faker.text(max_nb_chars=50)}"

    @staticmethod
    def generate_random_location():
        return random.choice(["MSK", "SPB"])

    @staticmethod
    def generate_random_genre():
        return random.randint(1, 10)

    @staticmethod
    def generate_random_page_size():
        return faker.random_int(min=1, max=10)

    @staticmethod
    def generate_random_page():
        return faker.random_int(min=1, max=10)

    @staticmethod
    def generate_random_min_price():
        return faker.random_int(min=1, max=100)

    @staticmethod
    def generate_random_max_price():
        return faker.random_int(min=101, max=1000)

    @staticmethod
    def generate_random_published_for_query():
        return random.choice(["true", "false"])

    @staticmethod
    def generate_random_published():
        return random.choice([True, False])

    @staticmethod
    def generate_random_created_at():
        return random.choice(["asc", "desc"])

    @staticmethod
    def generate_user_data() -> dict:
        from uuid import uuid4

        return {
            "id": f"{uuid4()}",
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

