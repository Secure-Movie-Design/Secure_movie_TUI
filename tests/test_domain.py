from datetime import datetime

import pytest
import requests_mock
from requests.exceptions import ConnectionError, JSONDecodeError
from valid8 import ValidationError

from movie.domain import Title, Description, Year, Category, Movie, Like, Email, Id, Password, Username, Director, \
    MovieDealer, ImageUrl


@pytest.fixture()
def mock_id():
    yield Id(0)


### Title ###
@pytest.mark.parametrize('values', [
    '',
    'A' * 51,
])
def test_invalid_title_raises_exception(values):
    with pytest.raises(ValidationError):
        Title(values)


@pytest.mark.parametrize('values', [
    1,
    1.0,
    True,
    [],
    {},
    (),
    object(),
])
def test_title_type_raises_exception(values):
    with pytest.raises(TypeError):
        Title(values)


@pytest.mark.parametrize('values', [
    'A',
    'A' * 50,
])
def test_title_format(values):
    assert Title(values).value == values


def test_title_str():
    assert str(Title('A title')) == 'A title'


def test_null_title_raises_exception():
    with pytest.raises(TypeError):
        Title(None)


### Description ###

@pytest.mark.parametrize('values', [
    '',
    'A' * 201,
    '@@@@@@@@'
])
def test_invalid_description_raises_exception(values):
    with pytest.raises(ValidationError):
        Description(values)


@pytest.mark.parametrize('values', [
    1,
    1.0,
    True,
    [],
    {},
    (),
    object(),
])
def test_invalid_description_type_raises_exception(values):
    with pytest.raises(TypeError):
        Description(values)


def test_description_format():
    assert Description('A description').value == 'A description'


def test_description_str():
    assert str(Description('A description')) == 'A description'


def test_null_description_raises_exception():
    with pytest.raises(TypeError):
        Description(None)


### Year ###

@pytest.mark.parametrize('values', [
    1899,
    datetime.now().year + 1,
])
def test_invalid_year_raises_exception(values):
    with pytest.raises(ValidationError):
        Year(values)


@pytest.mark.parametrize('values', [
    1.0,
    [],
    {},
    (),
    object(),
])
def test_invalid_year_type_raises_exception(values):
    with pytest.raises(TypeError):
        Year(values)


def test_year_format():
    assert Year(2020).value == 2020


def test_year_str():
    assert str(Year(2020)) == '2020'


def test_null_year_raises_exception():
    with pytest.raises(TypeError):
        Year(None)


### Category ###

@pytest.mark.parametrize('values', [
    'NONEXISTENT',
    '',
    'A' * 257,
    (),
    {},
    [],
    1,
    1.0,
    True,
    object(),
])
def test_invalid_category_type_raises_exception(values):
    with pytest.raises(TypeError):
        Category(values)


def test_category_format():
    assert Category(Category.MovieCategory.ACTION).value == Category.MovieCategory.ACTION


def test_category_str():
    assert str(Category(Category.MovieCategory.ACTION)) == 'ACTION'


def test_null_category_raises_exception():
    with pytest.raises(TypeError):
        Category(None)


### Director ###

@pytest.mark.parametrize('values', [
    'AA',  # too short
    'A' * 101,  # too long
    'A dir&ctor',  # special character
    'A d1rector',  # number
    'A director with an ending space ',  # ending space
    ' A director with a starting space',  # starting space
    'A director with a double  space',  # double space
    "A director with an invalid '",  # ' with space after
    "An 'invalid director",  # ' with space before
    'A d1irector',  # number
])
def test_invalid_director_raises_exception(values):
    with pytest.raises(ValidationError):
        Director(values)


@pytest.mark.parametrize('values', [
    'A dirctor\'s name',
    'A director',
])
def test_director_format(values):
    assert Director(values).value == values


def test_null_director_raises_exception():
    with pytest.raises(TypeError):
        Director(None)


def test_director_str():
    assert str(Director('A director')) == 'A director'


@pytest.mark.parametrize('values', [
    1,
    1.0,
    True,
    [],
    {},
    (),
    object(),
])
def test_director_type_raises_exception(values):
    with pytest.raises(TypeError):
        Director(values)


### ImageUrl ###
def test_null_image_url_raises_exception():
    with pytest.raises(TypeError):
        ImageUrl(None)


def test_image_url_str():
    assert (str(ImageUrl('https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg')) ==
            'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg')


def test_image_url_format():
    assert (ImageUrl('https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg').value ==
            'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg')


@pytest.mark.parametrize('values', [
    1,
    1.0,
    True,
    [],
    {},
    (),
    object(),
])
def test_invalid_image_url_raises_exception(values):
    with pytest.raises(TypeError):
        ImageUrl(values)


@pytest.mark.parametrize('values', [
    'https://image.tmdb.org/t/p/w500/a.jpg',
    'a',
    '',
    'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg' + 'a' * 200,
    'http://example.com'
])
def test_invalid_image_url_format_raises_exception(values):
    with pytest.raises(ValidationError):
        ImageUrl(values)


### Id ###
def test_null_id_raises_exception():
    with pytest.raises(TypeError):
        Id(None)


@pytest.mark.parametrize('values', [
    1.0,
    'a',
    [],
    {},
    (),
    object(),
])
def test_invalid_id_raises_exception(values):
    with pytest.raises(TypeError):
        Id(values)


def test_id_format():
    assert Id(1).value == 1


def test_id_str():
    assert str(Id(1)) == '1'


### Email ###

@pytest.mark.parametrize('values', [
    '',
    'invalid@email.example' + 'e' * 200,
    'invalidemail',
    'invalidemail@',
    'invalid.email.example',
    '@email.example',
    'email@example',
])
def test_invalid_email_raises_exception(values):
    with pytest.raises(ValidationError):
        Email(values)


@pytest.mark.parametrize('values', [
    'validemail@example.com',
    'valid.email@example.com',
])
def test_email_format(values):
    assert Email(values).value == values


def test_null_email_raises_exception():
    with pytest.raises(TypeError):
        Email(None)


def test_email_str():
    assert str(Email('email@example.com')) == 'email@example.com'


### Password ###

@pytest.mark.parametrize('values', [
    '',
    'a' * 7,  # too short
    'a' * 31,  # too long
    'a1@bcdefgh',  # no uppercase
    'A1@BCDEFGH',  # no lowercase
    'aA@bcdefgh',  # no number
    'aA1bcdefgh',  # no special character
])
def test_invalid_password_raises_exception(values):
    with pytest.raises(ValidationError):
        Password(values)


def test_password_format():
    assert Password('aA1@bcdefgh').value == 'aA1@bcdefgh'


def test_null_password_raises_exception():
    with pytest.raises(TypeError):
        Password(None)


def test_password_str():
    assert str(Password('P@Ssw0rd')) == 'P@Ssw0rd'


@pytest.mark.parametrize('values', [
    1,
    1.0,
    [],
    {},
    (),
    object(),
])
def test_invalid_password_type_raises_exception(values):
    with pytest.raises(TypeError):
        Password(values)


### Username ###

@pytest.mark.parametrize('values', [
    '',
    'a' * 31,  # too long
    'a b',  # space
    'a-b',  # dash
])
def test_invalid_username_raises_exception(values):
    with pytest.raises(ValidationError):
        Username(values)


@pytest.mark.parametrize('values', [
    'a',
    'a1',
    'a_',
])
def test_username_format(values):
    assert Username(values).value == values


def test_null_username_raises_exception():
    with pytest.raises(TypeError):
        Username(None)


def test_username_str():
    assert str(Username('username')) == 'username'


@pytest.mark.parametrize('values', [
    1,
    1.0,
    [],
    {},
    (),
    object(),
])
def test_invalid_username_type_raises_exception(values):
    with pytest.raises(TypeError):
        Username(values)


### Movie ###

def test_movie_type_is_movie(mock_id):
    movie = Movie(mock_id, Title('A title'), Description('A description'), Year(2020),
                  Category(Category.MovieCategory.ACTION), Director('A director'))
    assert movie.type == 'MOVIE'


def test_movie_str(mock_id):
    movie = Movie(mock_id, Title('A title'), Description('A description'), Year(2020),
                  Category(Category.MovieCategory.ACTION), Director('A director'))
    assert str(movie) == (f'Id: {mock_id.value}\n'
                          'Title: A title\n'
                          'Description: A description\n'
                          'Year: 2020\n'
                          'Category: ACTION\n'
                          'Director: A director\n')


def test_null_movie_title_raises_exception():
    with pytest.raises(TypeError):
        Movie(None, Description('A description'), Year(2020), Category(Category.MovieCategory.ACTION),
              Director('A director'))


def test_null_movie_description_raises_exception():
    with pytest.raises(TypeError):
        Movie(Title('A title'), None, Year(2020), Category(Category.MovieCategory.ACTION), Director('A director'))


def test_null_movie_year_raises_exception():
    with pytest.raises(TypeError):
        Movie(Title('A title'), Description('A description'), None, Category(Category.MovieCategory.ACTION))


def test_null_movie_category_raises_exception():
    with pytest.raises(TypeError):
        Movie(Title('A title'), Description('A description'), Year(2020), None, Director('A director'))


def test_null_movie_director_raises_exception():
    with pytest.raises(TypeError):
        Movie(Title('A title'), Description('A description'), Year(2020), Category(Category.MovieCategory.ACTION), None)


### Like ###

def test_like_str(mock_id):
    movie = Movie(mock_id, Title('A title'), Description('A description'), Year(2020),
                  Category(Category.MovieCategory.ACTION), Director('A director'))
    like = Like(mock_id, movie)
    assert str(like) == f'User ID: {mock_id.value}\nMovie: {movie.title}\n'


@pytest.fixture
def valid_movie(mock_id):
    return Movie(mock_id, Title('A title'), Description('A description'), Year(2020),
                 Category(Category.MovieCategory.ACTION), Director('A director'))


def test_null_like_liked_raises_exception(valid_movie, mock_id):
    with pytest.raises(TypeError):
        Like(mock_id, valid_movie, None)


@pytest.mark.parametrize('values', [
    1,
    1.0,
    [],
    {},
    (),
    object(),
])
def test_invalid_like_raises_exception(values):
    with pytest.raises(TypeError):
        Like(valid_movie, values)


### MovieDealer ###

@pytest.fixture
def movie_dealer():
    yield MovieDealer()


@pytest.fixture
def json_movie():
    return {'id': 1, 'title': 'Title 1', 'description': 'ADescription 1', 'year': 2020, 'category': 'ACTION',
            'director': 'A director', 'image_url': 'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg'}


@pytest.fixture
def movie():
    return (Title('A title'), Description('descr'), Year(2020), Category(Category.MovieCategory.ACTION),
            Director('A director'), ImageUrl('https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg'))


def test_signup_returns_correct_string_when_the_two_passwords_are_different(movie_dealer):
    assert movie_dealer.sign_up(Username('username'), Email('cioa@ciao.com'), Password('A_p@ssw0rd'),
                                Password('A_different_p@ssw0rd')) == "The two passwords are not the same."


def test_signup_raises_exception_when_invalid_fields(movie_dealer):
    with pytest.raises(ValidationError):
        movie_dealer.sign_up(Username(''), Email('cioa@ciao.com'), Password('A_p@ssw0rd'), Password('A_p@ssw0rd'))


def test_signup_returns_correct_string_when_registration_fails(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/registration', status_code=400)
        assert movie_dealer.sign_up(Username('username'), Email('cioa@ciao.com'), Password('A_p@ssw0rd'),
                                    Password('A_p@ssw0rd')) == "Something went wrong during user registration"


def test_signup_returns_correct_string_when_registration_succeeds(movie_dealer):
    username = 'username'
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/registration', status_code=204)
        assert movie_dealer.sign_up(Username(username), Email('cioa@ciao.com'), Password('A_p@ssw0rd'),
                                    Password('A_p@ssw0rd')) == f'Welcome in our app, {username}!'


def test_signup_returns_correct_string_when_connection_error(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/registration', exc=ConnectionError)
        assert movie_dealer.sign_up(Username('username'), Email('cioa@ciao.com'), Password('A_p@ssw0rd'),
                                    Password('A_p@ssw0rd')) == "Couldn't reach server..."


# TESTING LOGIN

def test_login_returns_token_when_successful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/login/', status_code=200,
                          json={'key': 'token'})
        assert movie_dealer.login(Username('username'), Password('A_p@ssw0rd')) == 'token'


def test_login_returns_none_when_connection_error(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/login/', exc=ConnectionError)
        assert movie_dealer.login(Username('username'), Password('A_p@ssw0rd')) is None


# TESTING LOGOUT

def test_logout_returns_true_when_successful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/logout/', status_code=200)
        assert movie_dealer.logout('token') is True


def test_logout_returns_false_when_unsuccessful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/auth/logout/', status_code=400)
        assert movie_dealer.logout('token') is False


# TESTING IS_ADMIN_USER

def test_is_admin_user_returns_true_when_user_is_admin(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.get('http://localhost:8000/api/v1/movies/user-type/',
                         json={'user-type': 'admin'})
        assert movie_dealer.is_admin_user('token') is True


def test_is_admin_user_returns_false_when_user_is_not_admin(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.get('http://localhost:8000/api/v1/movies/user-type/',
                         json={'user-type': 'user'})
        assert movie_dealer.is_admin_user('token') is False


# TESTING ADD LIKE

def test_add_like_returns_true_when_successful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/likes/', status_code=201)
        assert movie_dealer.add_like('token', Id(1)) is True


def test_add_like_returns_false_when_unsuccessful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/likes/', status_code=400)
        assert movie_dealer.add_like('token', Id(1)) is False


# TESTING REMOVE LIKE

def test_remove_like_returns_true_when_successful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.delete('http://localhost:8000/api/v1/likes/by_movie/1/', status_code=204)
        assert movie_dealer.remove_like('token', Id(1)) is True


def test_remove_like_returns_false_when_unsuccessful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.delete('http://localhost:8000/api/v1/likes/by_movie/1/', status_code=400)
        assert movie_dealer.remove_like('token', Id(1)) is False


# TESTING GET MOVIES


@pytest.mark.parametrize('values', [
    [{'id': 1, 'title': 'A title', 'description': 'A description', 'year': 2020,
      'category': 'ACTION', 'director': 'A director'}],
    [{'id': 1, 'title': 'A title', 'description': 'A description', 'year': 2020,
      'category': 'ACTION', 'director': 'A director'},
     {'id': 2, 'title': 'A title', 'description': 'A description', 'year': 2020,
      'category': 'ACTION', 'director': 'A director'}],
    [],
])
def test_get_movies_format(movie_dealer, values):
    with requests_mock.Mocker() as request_mock:
        request_mock.get('http://localhost:8000/api/v1/movies/', status_code=200,
                         json=values)
        assert movie_dealer.get_movies() == values


def test_get_movies_returns_empty_list_when_request_fails(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.get('http://localhost:8000/api/v1/movies/', status_code=400)
        assert movie_dealer.get_movies() == []


# TESTING ADD MOVIE

def test_add_movie_returns_true_when_successful(movie_dealer, movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/movies/', status_code=201)
        assert movie_dealer.add_movie('token', *movie) is True


def test_add_movie_raises_exception_with_invalid_movie(movie_dealer, movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.post('http://localhost:8000/api/v1/movies/', status_code=400)
        assert movie_dealer.add_movie('token', *movie) is False


# TESTING UPDATE MOVIE

def test_update_movie_returns_true_when_successful(movie_dealer, json_movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.put(f'http://localhost:8000/api/v1/movies/{json_movie["id"]}/', status_code=200)
        assert movie_dealer.update_movie('token', json_movie) is True


def test_update_movie_returns_falsee_when_unsuccessful(movie_dealer, json_movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.put(f'http://localhost:8000/api/v1/movies/{json_movie["id"]}/', status_code=400)
        assert movie_dealer.update_movie('token', json_movie) is False


# TESTING REMOVE MOVIE

def test_remove_movie_returns_true_when_successful(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.delete(f'http://localhost:8000/api/v1/movies/1/', status_code=204)
        assert movie_dealer.remove_movie('token', Id(1)) is True


def test_remove_movie_returns_true_when_unsuccessful(movie_dealer, json_movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.delete(f'http://localhost:8000/api/v1/movies/1/', status_code=400)
        assert movie_dealer.remove_movie('token', Id(1)) is False


# TESTING GET MOVIE BY ID


def test_get_movie_by_id_returns_movie_when_successful(movie_dealer, json_movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.get(f'http://localhost:8000/api/v1/movies/{json_movie["id"]}/', status_code=200,
                         json=json_movie)
        assert movie_dealer.get_movie(Id(json_movie["id"])) == json_movie


def test_get_movie_by_id_returns_none_when_unsuccessful(movie_dealer, json_movie):
    with requests_mock.Mocker() as request_mock:
        request_mock.get(f'http://localhost:8000/api/v1/movies/{json_movie["id"]}/', status_code=400,
                         json=json_movie)
        assert movie_dealer.get_movie(Id(json_movie["id"])) is None


# TESTING GET MOVIES SORTED BY TITLE

@pytest.mark.parametrize('values', [
    [{'id': 1, 'title': 'A title', 'description': 'A description', 'year': 2020,
      'category': 'ACTION', 'director': 'A director'}],
    [{'id': 1, 'title': 'B title', 'description': 'A description', 'year': 2020,
      'category': 'ACTION', 'director': 'A director'},
     {'id': 2, 'title': 'C title', 'description': 'A description', 'year': 2020,
      'category': 'ACTION', 'director': 'A director'}]
])
def test_get_movies_sorted_by_title_format(movie_dealer, values):
    with requests_mock.Mocker() as request_mock:
        request_mock.get('http://localhost:8000/api/v1/movies/sort-by-title/', status_code=200,
                         json=values)
        assert movie_dealer.sort_movies_by_title() == values


def test_get_movies_sorted_by_title_returns_empty_list_when_request_fails(movie_dealer):
    with requests_mock.Mocker() as request_mock:
        request_mock.get('http://localhost:8000/api/v1/movies/sort-by-title/', status_code=400)
        assert movie_dealer.sort_movies_by_title() == []
