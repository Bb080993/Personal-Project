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
    # print("ERROR HERE", book)
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
    # print("ID!!!", one_book_with_user.created_by.id)
    book_characters=Book.get_all_characters_from_book(data)
    print("BOOK CHARACTERS", book_characters)
    session["book_id"]=one_book_with_user.id
    # print("SESSION", session["book_id"])
    return render_template("oneBook.html", one_book_with_user=one_book_with_user, book_characters=book_characters)

@app.route('/edit/book/<int:id>')
def edit_book(id):
    if not "user_id" in session:
        return redirect("/")
    data={
        "id":id
    }
    one_book_with_user=Book.one_book_with_user(data)

    return render_template("editBook.html", one_book_with_user=one_book_with_user)

@app.route('/edit_form', methods=["POST"])
def update_book():
    data={
        "user_id": request.form['user_id'],
        "id": request.form['id'],
        "title": request.form['title'],
        "author": request.form['author'],
        "summary": request.form['summary']
    }
    if not Book.validate_new_summary(data):
        return redirect(f"/edit/book/{request.form['id']}")
    Book.edit_one_book(data)

    return redirect(f"/oneBook/{request.form['id']}")
       
@app.route('/search')
def search_page():
    if not "user_id" in session:
        return redirect("/")
    data={
        "title":session['title']
    }
    search_results=Book.search_by_title(data)
    print("SEARCH RESULTS", search_results)
    return render_template('search.html', search_results=search_results)

@app.route('/search_form', methods=['POST'])
def search_form():
    
    session['title']=request.form['title']
   
    # print("TITLE", session['title'])
    return redirect('/search')

@app.route('/delete/<int:id>')
def delete_book(id):
    if not "user_id" in session:
        return redirect("/")
    data={
        "id":id
    }
    Book.delete(data)

    return redirect('/my/books')