class Book(object):
    def __init__(self, isbn, title, description=None, category=None):
        self.isbn = isbn
        self.title = title
        self.description = description
        self.score = 0
        self.readers = []
        self.category = category

    def assign_rating(self, score):
        self.score = score

    def add_reader(self, user):
        self.readers.append(user)


class User(object):
    def __init__(self, name):
        self.username = name
        self.score = 0
        self.books_read = []
        self.users_followed = []

    def get_book_by_isbn(self, isbn):
        for book in self.books_read:
            if book.isbn == isbn:
                return book
        return None

    def follows(self, user):
        self.users_followed.append(user)

    def reads(self, book):
        assert isinstance(book, Book)
        self.books_read.append(book)
        book.add_reader(self)

    def increment_score(self, score):
        self.score = self.score + score
