from app import app
from flask import Flask, render_template, redirect, request, session, flash
from app.models.book_model import Book
from app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route('/createSummary')
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
    print("REQUEST ID", request.form["user_id"])
    data={
        "user_id":request.form["user_id"],
        "title":request.form["title"],
        "author":request.form["author"],
        "summary":request.form["summary"]
    } 
    # if validations check out, send info through form and into db
    Book.create_summary(data)
    return redirect("/home")