from app import app
from flask import Flask, render_template, redirect, request, session, flash
from app.models.book_model import Book
from app.models.user_model import User
from app.models.character_model import Character

@app.route('/character_form', methods=["POST"])
def addCharacter():
    print("REQUEST FORM", request.form['book_id'])
    if not Character.validate_character(request.form):
        return redirect(f"/oneBook/{request.form['book_id']}")
    # send through data dictionary to db query
    data={
        "book_id":request.form["book_id"],
        "name":request.form["name"],
        "description":request.form["description"]
    } 
    # if validations check out, send info through form and into db
    Character.add_character(data)
    return redirect(f"/oneBook/{request.form['book_id']}")

@app.route('/edit/character/<int:id>')
def edit_one_character(id):
    if not "user_id" in session:
        return redirect("/")
    data={
        "id":id
    
    }
    one_character=Character.find_character(data)
    # one_book_with_user=Book.one_book_with_user(data)
    # print("ONE CHARACTER", one_character)
    return render_template("editCharacter.html", one_character=one_character )

@app.route('/character_edit', methods=["POST"])
def update_character():
    print("BOOK ID", request.form["book_id"])
    if not Character.validate_character(request.form):
        return redirect(f"/edit/character/{request.form['id']}")
    data={
        "id":request.form['id'],
        "book_id":request.form["book_id"],
        "name":request.form["name"],
        "description":request.form["description"]
    } 
    Character.edit_character(data)
    return redirect(f"/oneBook/{request.form['book_id']}")

@app.route('/delete/character/<int:id>')
def delete_one_character(id):
    data={
        "id": id
    }
    Character.delete_character(data)
    return redirect(f"/oneBook/{session['book_id']}")
