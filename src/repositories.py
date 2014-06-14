class BooksRepository(object):
    def __init__(self):
        self.books = []

    def query_book_title(self, title):
        book_info = dict()
        return book_info

    def query_book_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None


class UsersRepository(object):
    def __init__(self):
        self.users = []

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        raise AssertionError

    def add_user(self, username):
        self.users.append(username)
