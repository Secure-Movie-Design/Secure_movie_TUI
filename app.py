import getpass
from typing import Any, Callable, Tuple

from typeguard import typechecked
from valid8 import ValidationError

from movie.domain import Email, MovieDealer, Password, Username, Id, Title, Description, Year, Category, Director, \
    ImageUrl, Movie
from movie.menu import Entry, Menu, MenuDescription


class App:
    def __init__(self):
        self.__menu = Menu.Builder(MenuDescription('Secure Movie Application Command line'),
                                   auto_select=lambda: print('Welcome to Secure Movie Design!')) \
            .with_entry(Entry.create('1', 'Sign up', on_selected=lambda: self.__sign_up())) \
            .with_entry(Entry.create('2', 'Login', on_selected=lambda: self.__login())) \
            .with_entry(Entry.create('3', 'Add like', on_selected=lambda: self.__addLike())) \
            .with_entry(Entry.create('4', 'Remove like', on_selected=lambda: self.__removeLike())) \
            .with_entry(Entry.create('5', 'Add movie', on_selected=lambda: self.__addMovie())) \
            .with_entry(Entry.create('6', 'Update movie', on_selected=lambda: self.__updateMovie())) \
            .with_entry(Entry.create('7', 'Remove movie', on_selected=lambda: self.__removeMovie())) \
            .with_entry(Entry.create('8', 'List liked movies', on_selected=lambda: self.__list_liked_movies())) \
            .with_entry(Entry.create('9', 'List movies', on_selected=lambda: self.__list_movies())) \
            .with_entry(Entry.create('10', 'Sort by title', on_selected=lambda: self.__sortByTitle())) \
            .with_entry(Entry.create('11', 'Filter by director', on_selected=lambda: self.__filter_by_director())) \
            .with_entry(Entry.create('12', 'Log out', on_selected=lambda: self.__logout())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('See you next time!'), is_exit=True)) \
            .build()
        self.__film_dealer = MovieDealer()
        self.__token = None

    def __list_movies(self):
        movies = self.__film_dealer.get_movies()
        if len(movies) == 0:
            print('No movies found...')
        else:
            self.__show_movies(movies)

    @typechecked
    def __show_movies(self, movies, title_str: str = 'ALL MOVIES'):
        def sep():
            print('-' * 120)

        fmt = '{:4}\t{:40}\t{:25}\t{:15}\t{:4}'

        print()
        sep()
        print(title_str)
        sep()
        print(fmt.format('ID', 'TITLE', 'DIRECTOR', 'CATEGORY', 'YEAR'))
        sep()
        for movie in movies:
            print(fmt.format(movie['id'], movie['title'], movie['director'], movie['category'], movie['year']))
        sep()
        print()

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
        self.__list_movies()

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

        self.__list_liked_movies()

        movie_id = self.__read_from_input("insert movie id", Id, to_convert=True)
        result = self.__film_dealer.remove_like(self.__token, movie_id)

        if result:
            print("Like removed successfully!")
        else:
            print(f"Couldn't remove like to the movie with id {movie_id}...")

    def __addMovie(self):
        if not self.__is_logged():
            print("You must be logged to add a movie!")
            return

        elif not self.__film_dealer.is_admin_user(self.__token):
            print("You must be admin to add a movie!")
            return

        result = self.__film_dealer.add_movie(self.__token, *self.__read_movie())

        if result:
            print("Movie added successfully!")
        else:
            print("Couldn't add the movie...")

    def __updateMovie(self):
        if not self.__is_logged():
            print("You must be logged to update a movie!")
            return

        elif not self.__film_dealer.is_admin_user(self.__token):
            print("You must be admin to update a movie!")
            return

        self.__list_movies()
        movie_id = self.__read_from_input("insert movie id", Id, to_convert=True)
        movie = self.__film_dealer.get_movie(movie_id)

        if movie is None:
            self.__error(f"Movie with id {movie_id.value} not found!")
            return

        movie_to_print = Movie(Id(movie['id']), Title(movie['title']), Description(movie['description']),
                               Year(movie['year']), Category(Category.MovieCategory[movie['category']]),
                               Director(movie['director']))
        print(movie_to_print)

        for f, c in self.__film_dealer.movie_fields:
            print(f"Do you want to update {f}? (y to update, n to skip)")
            if input().strip() == 'y':
                if f == 'category':
                    val = self.__read_category(f"Select a category (insert its number)")
                    movie[f] = val.value.name
                else:
                    val = self.__read_from_input(f"insert new {f}", c)
                    movie[f] = val.value

        result = self.__film_dealer.update_movie(self.__token, movie)

        if result:
            print("Movie updated successfully!")
        else:
            print("Couldn't update the movie...")

    def __removeMovie(self):
        if not self.__is_logged():
            print("You must be logged to remove a movie!")
            return

        elif not self.__film_dealer.is_admin_user(self.__token):
            print("You must be admin to remove a movie!")
            return

        self.__list_movies()
        movie_id = self.__read_from_input("insert movie id", Id, to_convert=True)
        movie = self.__film_dealer.get_movie(movie_id)

        if movie is None:
            self.__error(f"Movie with id {movie_id.value} not found!")
            return

        result = self.__film_dealer.remove_movie(self.__token, movie_id)

        if result:
            print("Movie removed successfully!")
        else:
            print("Couldn't remove the movie...")

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

    def __sortByTitle(self):
        movies = self.__film_dealer.sort_movies_by_title()
        if len(movies) == 0:
            print('No movies found...')
        else:
            self.__show_movies(movies, title_str='MOVIES SORTED BY TITLE')

    def __list_liked_movies(self):
        if not self.__is_logged():
            print("You must be logged to see your liked movies!")
            return

        movies = self.__film_dealer.get_liked_movies(self.__token)
        if len(movies) == 0:
            print('No movies found...')
        else:
            self.__show_movies(movies, title_str='USER LIKED MOVIES')

    def __filter_by_director(self):
        director = self.__read_from_input("insert director", Director)
        movies = self.__film_dealer.filter_movies_by_director(director)
        if len(movies) == 0:
            print('No movies found...')
        else:
            self.__show_movies(movies, title_str='MOVIES FILTERED BY DIRECTOR')

    def __read_movie(self) -> Tuple[Title, Description, Year, Category, Director, ImageUrl]:
        title = self.__read_from_input('Title', Title)
        description = self.__read_from_input('Description', Description)
        year = self.__read_from_input('Year', Year, to_convert=True)
        category = self.__read_category('Select a category (insert its number)')
        director = self.__read_from_input('Director', Director)
        image_url = self.__read_from_input('Image URL', ImageUrl)
        return title, description, year, category, director, image_url

    def __print_categories(self) -> None:
        categories = self.__film_dealer.categories_list
        print_sep = lambda: print('-' * 50)
        print_sep()
        fmt = '%3s %-30s'
        print(fmt % ('#', 'CATEGORY'))
        print_sep()
        for index in range(len(categories)):
            print(fmt % (str(index + 1), categories[index]))
        print_sep()

    @typechecked
    def __read_category(self, prompt: str) -> Any:
        while True:
            try:
                self.__print_categories()
                line = ''
                line = input(f'{prompt}: ').strip()
                res = Category(Category.MovieCategory(self.__film_dealer.categories_list[int(line) - 1]))
                return res
            except (TypeError, ValueError) as e:
                self.__error(f'Invalid value type.')

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
