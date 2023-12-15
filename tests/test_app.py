from unittest.mock import patch
import pytest
from datetime import date
from getpass import getpass

import requests_mock

from app import App, main
from movie.domain import MovieDealer

from movie.menu import Menu

from requests.exceptions import ConnectionError


@pytest.fixture
def app():
    yield App()


def test_read_from_input_validation_error():
    pass


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

@patch('builtins.input', side_effect=['2', 'username', '8', '0'])  # login -> logout -> terminazione programma
@patch('builtins.print')
def test_logout_prints_correctly_when_logout_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'logout', return_value=True) as logout:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
                app.run()
                mock_print.assert_any_call('Logout successful!')
                mock_print.assert_called()


@patch('builtins.input', side_effect=['8', '0'])  # logout -> terminazione programma
@patch('builtins.print')
def test_logout_prints_correctly_when_not_logged_in(mock_print, mock_input, app):
    app.run()
    mock_print.assert_any_call('You must be logged to logout!')
    mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '8', '0'])  # login -> logout -> terminazione programma
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


@patch('builtins.input', side_effect=['2', 'username', '3', '1', '0'])  # login -> username -> add like -> movie id -> terminazione programma
@patch('builtins.print')
def test_add_like_prints_correctly_when_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'add_like', return_value=True) as add_like:
                app.run()
                mock_print.assert_any_call("Like added successfully!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '3', '1', '0'])  # login -> username -> add like -> movie id -> terminazione programma
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


@patch('builtins.input', side_effect=['2', 'username', '4', '1', '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_remove_like_prints_correctly_when_successful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'remove_like', return_value=True) as remove_like:
                app.run()
                mock_print.assert_any_call("Like removed successfully!")
                mock_print.assert_called()


@patch('builtins.input', side_effect=['2', 'username', '4', '1', '0'])  # login -> username -> remove like -> movie id -> terminazione programma
@patch('builtins.print')
def test_remove_like_prints_correctly_when_unsuccessful(mock_print, mock_input, app):
    with patch.object(MovieDealer, 'login', return_value="token") as login:
        with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
            with patch.object(MovieDealer, 'remove_like', return_value=False) as remove_like:
                app.run()
                mock_print.assert_any_call(f"Couldn't remove like to the movie with id 1...")
                mock_print.assert_called()
