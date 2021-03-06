from flask import Flask, render_template, redirect, url_for
from models.models import *
from src import repositories
from functions.matchingfunction import get_recommended_books
app = Flask(__name__)


books_repo = repositories.BooksRepository()
users_repo = repositories.UsersRepository()


@app.route('/ping')
def hello_world_endpoint():
    return render_template('main.html', title="Main", content="Pong?")


@app.route('/user/<username>', methods=["GET", "POST"])
def user_page(username):
    user = users_repo.get_user(username)

    potentialbooks = sorted(sum(get_recommended_books(user), []), key=lambda x: x.score, reverse=True)
    output = []
    for item in potentialbooks:
        if item not in output and item not in user.books_read:
            output.append(item)
    if len(output) == 0:
        potentialbooks = books_repo.books
    else:
        potentialbooks = output

    if user:
        return render_template('user.html',
                               user=user,
                               allusers=users_repo.users,
                               potentialbooks=potentialbooks)
    else:
        return render_template('error.html')


@app.route("/user/<username>/follow/<anotheruser>")
def user_follows(username, anotheruser):
    first_user = users_repo.get_user(username)
    second_user = users_repo.get_user(anotheruser)
    first_user.follows(second_user)
    first_user.increment_score(1)
    return redirect(url_for('user_page', username=username))


@app.route("/user/<username>/read/<bookisbn>")
def user_reads(username, bookisbn):
    first_user = users_repo.get_user(username)
    book = books_repo.query_book_isbn(bookisbn)
    first_user.reads(book)
    first_user.increment_score(2)
    return redirect(url_for('user_page', username=username))


@app.route("/book/<isbn>")
def book_page(isbn):
    book = books_repo.query_book_isbn(isbn)
    return render_template('book.html', book=book)


@app.route("/user/<username>/rate/<isbn>/<rating>")
def rate_a_book(username, isbn, rating):
    user = users_repo.get_user(username)
    book = user.get_book_by_isbn(isbn)
    book.assign_rating(rating)
    user.increment_score(5)
    return redirect(url_for('user_page', username=user.username))


if __name__ == '__main__':
    app.debug = True

    # BEGIN MOCK USERS
    users = [User(name) for name in ["Tom", "John", "Mike"]]
    books = [Book(isbn="9788866543256", title="The Catcher in the Rye", category="Fiction"),
             Book(isbn="9788866546567", title="Cinderella", category="Children"),
             Book(isbn="9788866546568", title="Le Petit Prince", category="Children"),
             Book(isbn="9788866546786", title="Cancer Tropic", description="Lorem ipsum...", category="Fiction"),
             Book(isbn="97888663456467", title="Scorpion Tropic", description="Lorem ipsum...", category="Crime"),
             Book(isbn="9788866546566", title="The Most Beautiful Book in The World", description="Lorem ipsum...",
                  category="Romance")]

    for book in books:
        books_repo.books.append(book)

    for user in users:
        users_repo.add_user(user)

    # MIKE READS TWO BOOKS
    mike = users_repo.get_user("Mike")

    app.run(port=6667)
