from datetime import datetime

import pytest

from movie.domain import Title, Description, Year, Category, Movie, Like, Email, Id, Password, Username, Director
from valid8 import ValidationError


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
    'AA',           # too short
    'A' * 101,      # too long
    'A dir&ctor',   # special character
    'A d1rector',   # number
    'A director with an ending space ',     # ending space
    ' A director with a starting space',    # starting space
    'A director with a double  space',      # double space
    "A director with an invalid '",         # ' with space after
    "An 'invalid director",                 # ' with space before
    'A d1irector',                          # number
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
    'a' * 7,        # too short
    'a' * 31,       # too long
    'a1@bcdefgh',   # no uppercase
    'A1@BCDEFGH',   # no lowercase
    'aA@bcdefgh',   # no number
    'aA1bcdefgh',   # no special character
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
    'a' * 31,       # too long
    'a b',          # space
    'a-b',          # dash
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
                          'Category: ACTION\n')


def test_null_movie_title_raises_exception():
    with pytest.raises(TypeError):
        Movie(None, Description('A description'), Year(2020), Category(Category.MovieCategory.ACTION), Director('A director'))


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

