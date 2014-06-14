def get_recommended_books(user):
    users_books = [(book.isbn) for book in user.books_read]
    users_followed = [user for user in user.users_followed]
