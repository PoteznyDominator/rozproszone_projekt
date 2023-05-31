from app import db


class Recipe(db.Model):
  __tablename__ = "recipes"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String())
  ingredients = db.Column(db.String())
  instructions = db.Column(db.String())
  image_uri = db.Column(db.String())

  def __init__(self, name, desc, image_uri, ingredients, instructions):
    self.name = name
    self.description = desc
    self.image_uri = image_uri
    self.ingredients = ingredients
    self.instructions = instructions
