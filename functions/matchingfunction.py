def get_recommended_books(user):
    user_books = [(book.isbn) for book in user.books_read]
    users_followed = [user.books_read for user in user.users_followed]
    return users_followed

