import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique
from typing import Any

import requests
from requests.exceptions import ConnectionError
from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'^[\w\d]+(\s[\w\d]+)*$'),
                 help_msg="Title must be between 1 and 50 characters long.")

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=200, custom=pattern(r'^[\w\d]+(\s[\w\d]+)*$'),
                 help_msg="Description must be between 1 and 200 characters long.")

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Year:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=1900, max_value=datetime.now().year,
                 help_msg="Year must be between 1900 and current year.")

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True)
class Id:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('id', self.value, min_value=0, help_msg='Id must be an integer greater than or equal to 0.')

    def __str__(self) -> str:
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Category:
    @unique  # Enum class decorator that ensures only one name is bound to any one value.
    class MovieCategory(Enum):
        ROMANCE = "ROMANCE",
        ACTION = "ACTION",
        ADVENTURE = "ADVENTURE",
        COMEDY = "COMEDY"
        CRIME = "CRIME"
        DRAMA = "DRAMA"
        FANTASY = "FANTASY"
        HISTORICAL = "HISTORICAL"
        HORROR = "HORROR"
        MYSTERY = "MYSTERY"
        PSYCHOLOGICAL = "PSYCHOLOGICAL"
        SCIENCE_FICTION = "SCIENCE_FICTION"
        THRILLER = "THRILLER"
        WESTERN = "WESTERN"

    value: MovieCategory

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, custom=self._is_a_valid_category,
                 help_msg="Category must be chosen from the provided list.")

    def __str__(self) -> str:
        return self.value.name

    # todo: da testare
    @typechecked
    def _is_a_valid_category(self, value) -> bool:
        return value in self.MovieCategory.__members__.values()


@typechecked
@dataclass(frozen=True, order=True)
class Director:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=3, max_len=100, custom=pattern(r'^[a-zA-Z]+(\s[a-zA-Z]+\'?[a-zA-Z]*)*$'),
                 help_msg="Director name an surname must be between 1 and 50 characters long, and"
                          "can contain only letters and \"'\".")

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class ImageUrl:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=200,
                 custom=pattern(r'https://image\.tmdb\.org/t/p/w500/[a-zA-Z\d]{27}\.jpg'),
                 help_msg="Image URL must be at most 200 characters long and "
                          "must be an URL like this one: "
                          "https://image.tmdb.org/t/p/w500/abcdefghiABCDEFGH0123456789.jpg")

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Movie:
    id: Id
    title: Title
    description: Description
    year: Year
    category: Category
    director: Director

    def __post_init__(self):
        validate_dataclass(self)

    @property
    def type(self) -> str:
        return 'MOVIE'

    def __str__(self) -> str:
        return (f"Id: {self.id}\n"
                f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Year: {self.year}\n"
                f"Category: {self.category}\n"
                f"Director: {self.director}\n")


@typechecked
@dataclass(frozen=True, order=True)
class Like:
    user_id: Id
    movie: Movie

    def __post_init__(self):
        validate_dataclass(self)

    def __str__(self):
        return (f"User ID: {self.user_id}\n"
                f"Movie: {self.movie.title}\n")


@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=200, custom=pattern(r'^[\w\d\.]+@\w+\.\w+$'),
                 help_msg="Email must be a valid email address.")

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=8, max_len=30, custom=lambda res: self._is_valid(self.value),
                 help_msg="Password must be between 8 and 30 characters long and contain at least one uppercase letter,"
                          "one lowercase letter, one number and one special character.")

    def __str__(self):
        return str(self.value)

    @staticmethod
    def _is_valid(value) -> bool:
        # no lowercase
        if not any(c.islower() for c in value):
            return False
        # no uppercase
        if not any(c.isupper() for c in value):
            return False
        # no number
        if not any(c.isdigit() for c in value):
            return False
        # no special character
        if not any(not c.isalnum() for c in value):
            return False
        return True


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=30, custom=pattern(r'^[\w\d_]+$'),
                 help_msg="Username must be between 1 and 30 characters long, and can contain letters, "
                          "numbers and underscores (_).")

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True)
class MovieDealer:
    __api_server = 'http://localhost:8000/api/v1'

    categories_list = [cat.value for cat in Category.MovieCategory]
    movie_fields = [('title', Title), ('description', Description), ('year', Year), ('category', Category),
                    ('director', Director), ('image_url', ImageUrl)]

    @typechecked
    def sign_up(self, username: Username, email: Email, password: Password, confirm_password: Password):
        try:
            validate("signup.username", username)
            validate("signup.email", email)
            validate("signup.password", password)
            validate("signup.confirmPassword", confirm_password)

            if password.value != confirm_password.value:
                return "The two passwords are not the same."

            my_data = {
                'username': username.value,
                'email': email.value,
                'password1': password.value,
                'password2': confirm_password.value
            }
            res = requests.post(url=f'{self.__api_server}/auth/registration', data=my_data)
            if res.status_code != 204:
                return "Something went wrong during user registration"
            else:
                return f'Welcome in our app, {username.value}!'
        except ConnectionError:
            return "Couldn't reach server..."

    @typechecked
    def login(self, username: Username, password: Password) -> str | None:
        try:
            validate("login.username", username)
            validate("login.password", password)
            res = requests.post(url=f'{self.__api_server}/auth/login/',
                                data={'username': username.value, 'password': password.value})
            if res.status_code != 200:
                return None
        except ConnectionError as e:
            return None

        _json = res.json()
        return _json['key']

    @typechecked
    def logout(self, key: str) -> bool:
        res = requests.post(url=f'{self.__api_server}/auth/logout/', headers={'Authorization': f'Token {key}'})
        if res.status_code == 200:
            return True
        else:
            return False

    @typechecked
    def is_admin_user(self, key: str) -> bool:
        res = requests.get(url=f'{self.__api_server}/movies/user-type/', headers={'Authorization': f'Token {key}'})
        _json = res.json()
        return _json['user-type'] == 'admin'

    @typechecked
    def add_like(self, key: str, movie_id: Id) -> bool:
        res = requests.post(url=f'{self.__api_server}/likes/',
                            headers={'Authorization': f'Token {key}'},
                            data={'movie': movie_id.value})
        if res.status_code == 201:
            return True
        else:
            return False

    @typechecked
    def remove_like(self, key: str, movie_id: Id) -> bool:
        res = requests.delete(url=f'{self.__api_server}/likes/by_movie/{movie_id.value}/',
                              headers={'Authorization': f'Token {key}'})
        if res.status_code == 204:
            return True
        else:
            return False

    @typechecked
    def add_movie(self, key: str, title: Title, description: Description, year: Year, category: Category,
                  director: Director, image_url: ImageUrl) -> bool:
        data = {
            'title': title.value,
            'description': description.value,
            'year': year.value,
            'category': category.value.name,
            'director': director.value,
            'image_url': image_url.value
        }
        res = requests.post(url=f'{self.__api_server}/movies/', headers={'Authorization': f'Token {key}',
                                                                         'Content-Type': 'application/json'},
                            data=json.dumps(data))
        return res.status_code == 201

    @typechecked
    def update_movie(self, key: str, movie: Any) -> bool:
        res = requests.put(url=f'{self.__api_server}/movies/{movie["id"]}/',
                           headers={'Authorization': f'Token {key}',
                                    'Content-Type': 'application/json'},
                           data=json.dumps(movie))
        return res.status_code == 200

    @typechecked
    def remove_movie(self, key: str, movie_id: Id) -> bool:
        res = requests.delete(url=f'{self.__api_server}/movies/{movie_id.value}/',
                              headers={'Authorization': f'Token {key}'})
        return res.status_code == 204

    @typechecked
    def get_movies(self):
        res = requests.get(url=f'{self.__api_server}/movies/')
        if res.status_code == 200:
            _json = res.json()
            return _json
        else:
            return []

    @typechecked
    def get_movie(self, movie_id: Id):
        res = requests.get(url=f'{self.__api_server}/movies/{movie_id.value}/')
        if res.status_code == 200:
            _json = res.json()
            return _json
        else:
            return None

    def sort_movies_by_title(self):
        res = requests.get(url=f'{self.__api_server}/movies/sort-by-title/')
        if res.status_code == 200:
            _json = res.json()
            return _json
        else:
            return []
