import os

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your secret key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Recipe


@app.route('/')
def home():
  data = Recipe.query.all()
  return render_template('recipe-box.html', data=data)


@app.route('/add-recipe', methods=["POST", "GET"])
def add_recipe():
  if request.method == "POST":
    name = request.form["name"]
    desc = request.form["description"]
    file = request.files["file"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]

    file_uri = ""
    if file:
      filename = secure_filename(file.filename)
      file_uri = os.path.join('static/images', filename)
      file.save(file_uri)

    if not name or not desc or not file or not ingredients or not instructions:
      flash("Formularz nie może zawierać pustych danych")
      return render_template('add-recipe-form.html')

    recipe = Recipe(name, desc, file_uri, ingredients, instructions)
    db.session.add(recipe)
    db.session.commit()
    return redirect("/")

  return render_template('add-recipe-form.html')


@app.route('/recipe/<recipe_id>', methods=["POST", "GET"])
def recipe_details(recipe_id):
  recipe = Recipe.query.get_or_404(recipe_id)
  return render_template('recipe_detail.html', recipe=recipe)


@app.route('/recipe/update/<recipe_id>',  methods=["POST", "GET"])
def recipe_update(recipe_id):
  recipe = Recipe.query.get_or_404(recipe_id)

  if request.method == "POST":
    name = request.form["name"]
    desc = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    file = request.files["file"]

    if not name or not desc or not ingredients or not instructions:
      flash("Formularz nie może zawierać pustych danych")
      return render_template('add-recipe-form.html', recipe=recipe, editing_mode=True)

    recipe.name = name
    recipe.description = desc
    recipe.ingredients = ingredients
    recipe.instructions = instructions

    if file:
      filename = secure_filename(file.filename)
      recipe.image_uri = os.path.join('static/images', filename)
      file.save(recipe.image_uri)

    db.session.commit()
    return redirect("/")

  return render_template('add-recipe-form.html', recipe=recipe, editing_mode=True)


@app.route('/recipe/delete/<recipe_id>')
def recipe_delete(recipe_id):
  recipe = Recipe.query.get_or_404(recipe_id)

  try:
    db.session.delete(recipe)
    db.session.commit()
    return redirect("/")
  except:
    return "There was a problem while deleting that item. Try again later."


if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
