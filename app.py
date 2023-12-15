import getpass
from typing import Any, Callable
from typeguard import typechecked
from valid8 import ValidationError
from movie.menu import Entry, Menu, Description
from movie.domain import Email, Movie, MovieDealer, Password, Username, Id


# implementare add_like
# implementare remove_like


# implementare add_movie (admin) (5)
# implementare remove_movie (admin) (6)
# implementare edit_movie (admin) (7)

# ???
# implementare movie filtrati
# implementare movie ordinati
# implementare lista movie a cui l'utente ha messo like

class App:
    def __init__(self):
        self.__menu = Menu.Builder(Description('Secure Movie Application Command line'),
                                   auto_select=lambda: print('Welcome to Secure Movie Design!')) \
            .with_entry(Entry.create('1', 'Sign up', on_selected=lambda: self.__sign_up())) \
            .with_entry(Entry.create('2', 'Login', on_selected=lambda: self.__login())) \
            .with_entry(Entry.create('3', 'Add like', on_selected=lambda: self.__addLike())) \
            .with_entry(Entry.create('4', 'Remove like', on_selected=lambda: self.__removeLike())) \
            .with_entry(Entry.create('8', 'Log out', on_selected=lambda: self.__logout())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('See you next time!'), is_exit=True)) \
            .build()
        self.__film_dealer = MovieDealer()
        self.__token = None

    def __sign_up(self):
        username = self.__read_from_input("insert username", Username)
        email = self.__read_from_input("insert email", Email)
        password = self.__read_from_input("insert password", Password, password=True)
        confirm_password = self.__read_from_input("insert password again", Password, password=True)
        print(self.__film_dealer.sign_up(username, email, password, confirm_password))

    def __login(self):

        if self.__is_logged():
            print("You are already logged!")
            return

        username = self.__read_from_input("insert username", Username)
        password = self.__read_from_input("insert password", Password, password=True)
        token = self.__film_dealer.login(username, password)
        if token is None:
            print("Login failed!")
            return
        self.__token = token
        print("Logged successfully!")

    def __addLike(self):
        if not self.__is_logged():
            print("You must be logged to add like!")
            return

        movie_id = self.__read_from_input("insert movie id", Id, to_convert=True)
        result = self.__film_dealer.add_like(self.__token, movie_id)

        if result:
            print("Like added successfully!")
        else:
            print(f"Couldn't like the movie with id {movie_id}...")

    def __removeLike(self):
        if not self.__is_logged():
            print("You must be logged to remove like!")
            return

        movie_id = self.__read_from_input("insert movie id", Id, to_convert=True)
        result = self.__film_dealer.remove_like(self.__token, movie_id)

        if result:
            print("Like removed successfully!")
        else:
            print(f"Couldn't remove like to the movie with id {movie_id}...")

    def __logout(self):
        if not self.__is_logged():
            print("You must be logged to logout!")
            return

        result = self.__film_dealer.logout(self.__token)
        if result:
            print("Logout successful!")
            self.__token = None
        else:
            print("Logout failed!")

    @typechecked
    def __read_from_input(self, prompt: str, builder: Callable, password: bool = False,
                          to_convert: bool = False) -> Any:
        while True:
            try:
                line = ''
                if password:
                    line = getpass.getpass(f'{prompt}: ').strip()
                else:
                    line = input(f'{prompt}: ').strip()
                if to_convert:
                    line = int(line.strip())
                res = builder(line)
                return res
            except ValidationError as e:
                self.__error(f'Invalid {prompt}.\n {e.help_msg}')
            except (TypeError, ValueError) as e:
                self.__error(f'Invalid value type.')

    @staticmethod
    @typechecked
    def __error(error_message: str):
        print(error_message)

    def __is_logged(self):
        return self.__token is not None

    def run(self):
        self.__menu.run()


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
