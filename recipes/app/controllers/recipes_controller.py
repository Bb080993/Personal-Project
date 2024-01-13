from app import app
from flask import Flask, render_template, redirect, request,session, flash
from app.models.user_model import User
from app.models.recipe_model import Recipe

@app.route("/create/recipe")
def create_new_recipe_page():
    if not "user_id" in session:
        return redirect("/")

    return render_template("create_recipe.html")

@app.route("/add_recipe", methods=["POST"])
def add_recipe():

   
    if not Recipe.validate_new_recipe(request.form):
        return redirect("/create/recipe")
    

    data={
        "user_id":request.form["user_id"],
        "name":request.form["name"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "date_cooked":request.form["date_cooked"],
        "less_than_30":request.form["less_than_30"]
    } 
    Recipe.create_recipe(data)
    return redirect("/recipes")

@app.route("/view/recipe/<int:id>")
def view_one_recipe(id):
    if not "user_id" in session:
        return redirect("/")
    data={
        "id":id
    }
    one_recipe_with_user=Recipe.one_recipe_with_user(data)

    return render_template("one_recipe.html", one_recipe_with_user=one_recipe_with_user)

@app.route("/edit/recipe/<int:id>")
def edit_recipe_page(id):
    if not "user_id" in session:
        return redirect("/")
    data={
        "id":id
    }
    one_recipe_with_user=Recipe.one_recipe_with_user(data)
    return render_template("edit_recipe.html", one_recipe_with_user=one_recipe_with_user)

@app.route("/edit_recipe", methods=["POST"])
def edit_one_recipe():
    data={
        "id":request.form["id"],
        "name":request.form["name"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "date_cooked":request.form["date_cooked"],
        "less_than_30":request.form["less_than_30"]
    }
    if not Recipe.validate_new_recipe(data):
        return redirect(f"/edit/recipe/{request.form['id']}")
    Recipe.update_recipe(data)

    return redirect("/recipes")

@app.route("/delete/recipe/<int:id>")
def delete_recipe(id):
    data={
        "id":id
    }
    Recipe.delete_a_recipe(data)
    return redirect('/recipes')