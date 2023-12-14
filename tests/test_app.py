from unittest.mock import patch
import pytest
from datetime import date
from getpass import getpass

import requests_mock


from app import App, main
from movie.domain import MovieDealer

from movie.menu import Menu


def test_read_from_input_validation_error():
    

@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_main(mock_print, mock_input):
    main('__main__')
    mock_print.assert_any_call('See you next time!')
    mock_print.assert_called()


# SIGN IN OPERATION TEST
@patch('builtins.input', side_effect=['1','username','test@email.it','0'])
@patch('builtins.print')
def test_signin_password_not_match(mock_print,mock_input):
    new_app = App()
    with patch('getpass.getpass', side_effect=['Password43210wewe?','Password43210wewe!']) as password:
        new_app.run()
        assert password.call_count == 2
        mock_print.assert_any_call("The two passwords are not the same.")
        mock_print.assert_called()


@patch('builtins.input', side_effect=['1','username','test@email.it','0'])
@patch('builtins.print')
def test_signin_fail(mock_print,mock_input):
    new_app = App()
    with patch('getpass.getpass', side_effect=['Password43210wewe?','Password43210wewe?']) as password:
         with requests_mock.Mocker() as request_mock:
            request_mock.post('http://localhost:8000/api/v1/auth/registration', status_code=400)
            new_app.run()
            assert password.call_count == 2
            mock_print.assert_any_call("Something went wrong during user registration")
            mock_print.assert_called()

@patch('builtins.input', side_effect=['1','username','test@email.it','0'])
@patch('builtins.print')
def test_signin_success(mock_print,mock_input):
    new_app = App()
    with patch('getpass.getpass', side_effect=['Password43210wewe?','Password43210wewe?']) as password:
         with requests_mock.Mocker() as request_mock:
            request_mock.post('http://localhost:8000/api/v1/auth/registration', status_code=204)
            new_app.run()
            assert password.call_count == 2
            mock_print.assert_any_call("Welcome in our app, username!")
            mock_print.assert_called()


# LOGIN OPERATION TEST

@patch('builtins.input', side_effect=['2','0'])
@patch('builtins.print')
def test_login_already(mock_print,mock_input):
    new_app = App()
    with patch.object(App, '_App__is_logged', return_value=True) as logMod:
        new_app.run()
        mock_print.assert_any_call('You are already logged!')
        mock_print.assert_called()


@patch('builtins.input', side_effect=['2','username','0'])
@patch('builtins.print')
def test_login_success(mock_print,mock_input):
    new_app = App()
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value="token") as login:
            new_app.run()
            password.assert_called_once()
            login.assert_called_once()
            mock_print.assert_any_call('Logged successfully!')

@patch('builtins.input', side_effect=['2','username','0'])
@patch('builtins.print')
def test_login_fail(mock_print,mock_input):
    new_app = App()
    with patch('getpass.getpass', side_effect=['Password43210wewe?']) as password:
        with patch.object(MovieDealer, 'login', return_value=None) as login:
            new_app.run()
            password.assert_called_once()
            login.assert_called_once()
            mock_print.assert_any_call('Login failed!')