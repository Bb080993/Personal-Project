from app import app
from flask import Flask, render_template, redirect, request, session, flash
from app.models.book_model import Book
from app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


# this page has the form to create a book summary
@app.route('/createSummary')
#make sure user is logged in otherwise they get redirected to login page
def createSummaryPage():
    if not "user_id" in session:
        return redirect("/")
    
    data={
        "id": session["user_id"]
    }
    user=User.get_user_by_id(data)
    return render_template("createSummary.html", user=user)

@app.route('/createSummaryForm', methods=["POST"])
def createSummaryForm():

    # need to create book model and validate_new_summary validations
    if not Book.validate_new_summary(request.form):
        return redirect("/createSummary")
    # send through data dictionary to db query
    data={
        "user_id":request.form["user_id"],
        "title":request.form["title"],
        "author":request.form["author"],
        "summary":request.form["summary"]
    } 
    # if validations check out, send info through form and into db
    book=Book.create_summary(data)
    print("ERROR HERE", book)
    return redirect(f"/oneBook/{book}")

@app.route('/my/books')
def my_books():
    if not "user_id" in session:
        return redirect("/")
    
    data={
        "id": session["user_id"]
    }
    all_books=Book.books_by_user(data)
    return render_template("myBooks.html", all_books=all_books)

@app.route('/oneBook/<int:id>')
def one_book(id):
    if not "user_id" in session:
        return redirect("/")
    data={
        "id":id
    }
    one_book_with_user=Book.one_book_with_user(data)

    return render_template("oneBook.html", one_book_with_user=one_book_with_user)