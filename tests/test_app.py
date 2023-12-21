from unittest.mock import patch
import pytest
from datetime import date
from getpass import getpass

import requests_mock

from app import App, main
from movie.domain import MovieDealer, Title, Movie, Description, Year, Director, Category, Id

from movie.menu import Menu

from requests.exceptions import ConnectionError


@pytest.fixture
def app():
    yield App()


@pytest.fixture
def movie():
    return {"id": 1, "title": "A title", "description": "A description", "year": 2020, "category": "ACTION", "director": "A director", "image_url": "https://image.tmdb.org/t/p/w500/eQ4GRmP0EEkxjwlPbZlVn7HLoZp.jpg"}


@pytest.fixture
def movies():
    return [Movie(Id(1), Title('A title'), Description('A description'), Year(2020), Category(Category.MovieCategory.ACTION), Director('A director')),
            Movie(Id(2), Title('B title'), Description('A description'), Year(2020), Category(Category.MovieCategory.ACTION), Director('A director')),
            Movie(Id(3), Title('C title'), Description('A description'), Year(2020), Category(Category.MovieCategory.ACTION), Director('A director'))]

@patch('builtins.input', side_effect=['1', 'username', 'emailwrong', 'email@libero.it', '0'])
@patch('builtins.print')
def test_read_input_validation_error(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?', 'Password43210wewe!']) as password:
        app.run()
        mock_print.assert_any_call("Invalid insert email.\n Email must be a valid email address.")
        mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '4', 'notanumber', '1',
                                      '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_read_input_type_error(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'remove_like', return_value=True) as remove_like:
                app.run()
                mock_print.assert_any_call("Invalid value type.")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_main(mock_print, mock_input):
    main('__main__')
    mock_print.assert_any_call('See you next time!')
    mock_print.assert_called()


# SIGN UP OPERATION TEST
@patch('builtins.input', side_effect=['1', 'username', 'test@email.it', '0'])
@patch('builtins.print')
def test_signup_password_not_match(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?', 'Password43210wewe!']) as password:
        app.run()
        assert password.call_count == 2
        mock_print.assert_any_call("The two passwords are not the same.")
        mock_print.assert_called()


@patch('builtins.input', side_effect=['1', 'username', 'test@email.it', '0'])
@patch('builtins.print')
def test_signup_fail(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?', 'Password43210wewe?']) as password:
        with requests_mock.Mocker() as request_mock:
            request_mock.post('http://localhost:8000/api/v1/auth/registration', status_code=400)
            app.run()
            assert password.call_count == 2
            mock_print.assert_any_call("Something went wrong during user registration")
            mock_print.assert_called()


@patch('builtins.input', side_effect=['1', 'username', 'test@email.it', '0'])
@patch('builtins.print')
def test_signup_prints_correctly_after_connection_error(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?', 'Password43210wewe?']) as password:
        with requests_mock.Mocker() as request_mock:
            request_mock.post('http://localhost:8000/api/v1/auth/registration', exc=ConnectionError)
            app.run()
            mock_print.assert_any_call("Couldn't reach server...")
            mock_print.assert_called()


@patch('builtins.input', side_effect=['1', 'username', 'test@email.it', '0'])
@patch('builtins.print')
def test_signup_success(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?', 'Password43210wewe?']) as password:
        with requests_mock.Mocker() as request_mock:
            request_mock.post('http://localhost:8000/api/v1/auth/registration', status_code=204)
            app.run()
            assert password.call_count == 2
            mock_print.assert_any_call("Welcome in our app, username!")
            mock_print.assert_called()


# LOGIN OPERATION TEST

@patch('builtins.input', side_effect=['2', '0'])
@patch('builtins.print')
def test_login_already(mock_print, mock_input, app):
    with patch.object(App, '_App__is_logged', return_value=True) as logMod:
        app.run()
        mock_print.assert_any_call('You are already logged!')
        mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '0'])
@patch('builtins.print')
def test_login_success(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            app.run()
            password.assert_called_once()
            login.assert_called_once()
            mock_print.assert_any_call('Logged successfully!')


@patch('builtins.input', side_effect=['2', 'username', '0'])
@patch('builtins.print')
def test_login_fail(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value=None) as login:
            app.run()
            password.assert_called_once()
            login.assert_called_once()
            mock_print.assert_any_call('Login failed!')


# LOGOUT OPERATION TEST

@patch('builtins.input', side_effect=['2', 'username', '12', '0'])  # login -> logout -> terminazione programma
@patch('builtins.print')
def test_logout_prints_correctly_when_logout_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'logout', return_value=True) as logout:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
                app.run()
                mock_print.assert_any_call('Logout successful!')
                mock_print.assert_called()


@patch('builtins.input', side_effect=['12', '0'])  # logout -> terminazione programma
@patch('builtins.print')
def test_logout_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call('You must be logged to logout!')
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '12', '0'])  # login -> logout -> terminazione programma
@patch('builtins.print')
def test_logout_prints_correctly_when_logout_fails(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'logout', return_value=False) as logout:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
                app.run()
                mock_print.assert_any_call("Logout failed!")
                mock_print.assert_called()


# ADD LIKE OPERATION TEST

@patch('builtins.input', side_effect=['3', '0'])  # add like -> id movie -> terminazione programma
@patch('builtins.print')
def test_add_like_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call("You must be logged to add like!")
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '3', '1',
                                      '0'])  # login -> username -> add like -> movie id -> terminazione programma
@patch('builtins.print')
def test_add_like_prints_correctly_when_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'add_like', return_value=True) as add_like:
                app.run()
                mock_print.assert_any_call("Like added successfully!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '3', '1',
                                      '0'])  # login -> username -> add like -> movie id -> terminazione programma
@patch('builtins.print')
def test_add_like_prints_correctly_when_unsuccessful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'add_like', return_value=False) as add_like:
                app.run()
                mock_print.assert_any_call(f"Couldn't like the movie with id 1...")
                mock_print.assert_called()


# REMOVE LIKE OPERATION TEST
@patch('builtins.input', side_effect=['4', '0'])  # remove like -> id movie -> terminazione programma
@patch('builtins.print')
def test_remove_like_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call("You must be logged to remove like!")
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '4', '1',
                                      '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_remove_like_prints_correctly_when_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'remove_like', return_value=True) as remove_like:
                app.run()
                mock_print.assert_any_call("Like removed successfully!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '4', '1',
                                      '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_remove_like_prints_correctly_when_unsuccessful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'remove_like', return_value=False) as remove_like:
                app.run()
                mock_print.assert_any_call(f"Couldn't remove like to the movie with id 1...")
                mock_print.assert_called()


# ADD MOVIE TEST

@patch('builtins.input', side_effect=['5', '0'])  # add movie -> terminazione programma
@patch('builtins.print')
def test_add_movie_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call("You must be logged to add a movie!")
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '5', '0'])  # add movie -> terminazione programma
@patch('builtins.print')
def test_add_movie_prints_correctly_when_not_admin_user(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch('movie.domain.MovieDealer.is_admin_user', return_value=False) as is_admin_user:
                app.run()
                mock_print.assert_any_call("You must be admin to add a movie!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '5', 'title', 'film descr', '2020', '12', 'Stanley Kubrick',
                                      'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
                                      '0'])  # add movie -> terminazione programma
@patch('builtins.print')
def test_add_movie_prints_correctly_when_successful(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                with patch.object(MovieDealer, 'add_movie', return_value=True) as add_movie:
                    app.run()
                    mock_print.assert_any_call("Movie added successfully!")
                    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '5', 'title', 'film descr', '2020', '12', 'Stanley Kubrick',
                                      'https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg',
                                      '0'])  # add movie -> terminazione programma
@patch('builtins.print')
def test_add_movie_prints_correctly_when_unsuccessful(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                with patch.object(MovieDealer, 'add_movie', return_value=False) as add_movie:
                    app.run()
                    mock_print.assert_any_call("Couldn't add the movie...")
                    mock_print.assert_called()


# UPDATE MOVIE TEST

@patch('builtins.input', side_effect=['6', '0'])  # update movie -> terminazione programma
@patch('builtins.print')
def test_update_movie_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call("You must be logged to update a movie!")
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '6', '0'])  # update movie -> terminazione programma
@patch('builtins.print')
def test_update_movie_prints_correctly_when_not_admin_user(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=False) as is_admin_user:
                app.run()
                mock_print.assert_any_call("You must be admin to update a movie!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '6', '1', '0'])  # update movie -> terminazione programma
@patch('builtins.print')
def test_update_movie_prints_correctly_when_movie_not_found(mock_print, mock_input, app, movie):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                with patch.object(MovieDealer, 'get_movie', return_value=None):
                    app.run()
                    mock_print.assert_any_call(f"Movie with id {movie['id']} not found!")
                    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '6', '1', 'y', 'new updated title', 'n', 'n', 'n', 'n', 'n', '0'])  # update movie -> terminazione programma
@patch('builtins.print')
def test_update_movie_prints_correctly_when_successful(mock_print, mock_input, app, movie):
     with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
         with patch.object(MovieDealer, 'login', return_value="token") as login:
             with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                 with patch.object(MovieDealer, 'get_movie', return_value=movie):
                     with patch.object(MovieDealer, 'update_movie', return_value=True):
                         app.run()
                         assert is_admin_user.called
                         mock_print.assert_any_call("Movie updated successfully!")
                         mock_print.assert_called()


# REMOVE MOVIE TEST

@patch('builtins.input', side_effect=['7', '0'])  # remove movie -> terminazione programma
@patch('builtins.print')
def test_remove_movie_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call("You must be logged to remove a movie!")
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '7', '0'])  # remove movie -> terminazione programma
@patch('builtins.print')
def test_remove_movie_prints_correctly_when_not_admin_user(mock_print, mock_input, app):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=False) as is_admin_user:
                app.run()
                mock_print.assert_any_call("You must be admin to remove a movie!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '7', '1', '0'])  # remove movie -> terminazione programma
@patch('builtins.print')
def test_remove_movie_prints_correctly_when_movie_not_found(mock_print, mock_input, app, movie):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                with patch.object(MovieDealer, 'get_movie', return_value=None):
                    app.run()
                    mock_print.assert_any_call(f"Movie with id {movie['id']} not found!")
                    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '7', '1', '0'])  # remove movie -> terminazione programma
@patch('builtins.print')
def test_remove_movie_prints_correctly_when_successful(mock_print, mock_input, app, movie):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                with patch.object(MovieDealer, 'get_movie', return_value=movie):
                    with patch.object(MovieDealer, 'remove_movie', return_value=True):
                        app.run()
                        mock_print.assert_any_call("Movie removed successfully!")
                        mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '7', '1', '0'])  # remove movie -> terminazione programma
@patch('builtins.print')
def test_remove_movie_prints_correctly_when_unsuccessful(mock_print, mock_input, app, movie):
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch.object(MovieDealer, 'is_admin_user', return_value=True) as is_admin_user:
                with patch.object(MovieDealer, 'get_movie', return_value=movie):
                    with patch.object(MovieDealer, 'remove_movie', return_value=False):
                        app.run()
                        mock_print.assert_any_call("Couldn't remove the movie...")
                        mock_print.assert_called()


# SHOW ALL MOVIES OPERATION TEST

@patch('builtins.input', side_effect=['9', '0'])  # list movies -> terminazione programma
@patch('builtins.print')
def test_list_movies_prints_correctly_when_no_movies_found(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'get_movies', return_value=[]) as get_movies:
        app.run()
        mock_print.assert_any_call("No movies found...")
        mock_print.assert_called()


@patch('builtins.input', side_effect=['9', '0'])  # list movies -> terminazione programma
@patch('builtins.print')
def test_show_movies_prints_correctly(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'get_movies', return_value=[{"id": 1, "title": "title", "description": "description",
                                                                "year": 2020, "category": "category",
                                                                "image_url": "image_url",
                                                                "director": "director"}]) as get_movies:
        app.run()
        mock_print.assert_any_call("ALL MOVIES")
        mock_print.assert_any_call(
            '{:4}\t{:40}\t{:25}\t{:15}\t{:4}'.format('ID', 'TITLE', 'DIRECTOR', 'CATEGORY', 'YEAR'))


# SORT MOVIES BY TITLE OPERATION TEST

@patch('builtins.input', side_effect=['10', '0'])  # sort movies by title -> terminazione programma
@patch('builtins.print')
def test_sort_movies_by_title_prints_correctly_when_no_movies_found(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'sort_movies_by_title', return_value=[]) as get_movies:
        app.run()
        mock_print.assert_any_call("No movies found...")
        mock_print.assert_called()


@patch('builtins.input', side_effect=['10', '0'])  # list movies -> terminazione programma
@patch('builtins.print')
def test_show_movies__sorted_by_title_prints_correctly(mock_print, mock_input, app, movies):
    with patch.object(MovieDealer, 'get_movies', return_value=movies) as get_movies:
        app.run()
        mock_print.assert_any_call('MOVIES SORTED BY TITLE')
        mock_print.assert_any_call(
            '{:4}\t{:40}\t{:25}\t{:15}\t{:4}'.format('ID', 'TITLE', 'DIRECTOR', 'CATEGORY', 'YEAR'))


# LIST LIKED MOVIED OPERATION TEST

@patch('builtins.input', side_effect=['8', '0'])  # remove movie -> terminazione programma
@patch('builtins.print')
def test_list_liked_movies_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call("You must be logged to see your liked movies!")
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '8',
                                      '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_list_liked_movies_prints_correctly_when_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'get_liked_movies',
                              return_value=[{"id": 1, "title": "title", "description": "description",
                                                                        "year": 2020, "category": "category",
                                                                        "image_url": "image_url",
                                                                        "director": "director"}]) as get_liked_movies:
                app.run()
                mock_print.assert_any_call("USER LIKED MOVIES")
                mock_print.assert_any_call(
                    '{:4}\t{:40}\t{:25}\t{:15}\t{:4}'.format('ID', 'TITLE',
                                                             'DIRECTOR', 'CATEGORY', 'YEAR'))


@patch('builtins.input', side_effect=['2', 'username', '8',
                                      '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_list_liked_movies_prints_correctly_when_unsuccessful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'get_liked_movies', return_value=[]) as get_liked_movies:
                app.run()
                mock_print.assert_any_call("No movies found...")
                mock_print.assert_called()


