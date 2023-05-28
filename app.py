import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Recipe(db.Model):
  __tablename__ = "recipes"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String())
  image_uri = db.Column(db.String())

  def __init__(self, name, desc, image_uri):
    self.name = name
    self.description = desc
    self.image_uri = image_uri


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

    file_uri = ""
    if file:
      filename = secure_filename(file.filename)
      file_uri = os.path.join('static/images', filename)
      file.save(file_uri)

    recipe = Recipe(name, desc, file_uri)
    db.session.add(recipe)
    db.session.commit()
    return redirect("/")

  return render_template('add-recipe-form.html')


@app.route('/recipe/<recipe_id>')
def recipe_details(recipe_id):
  recipe = Recipe.query.get(recipe_id)

  return render_template('recipe_detail.html', recipe=recipe)


if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
