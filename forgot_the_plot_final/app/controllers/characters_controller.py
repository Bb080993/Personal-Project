from app import app
from flask import Flask, render_template, redirect, request, session, flash
from app.models.book_model import Book
from app.models.user_model import User
from app.models.character_model import Character

@app.route('/character_form/<int:id>')
def addCharacter(id):
    if not Character.validate_character(request.form):
        return redirect(f"/oneBook/${id}")
    # send through data dictionary to db query
    data={
        "book_id":request.form["book_id"],
        "name":request.form["name"],
        "description":request.form["description"]
    } 
    # if validations check out, send info through form and into db
    Character.add_character(data)
    return redirect(f"/oneBook/${id}")

