from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(100)) # ISBN can be 10 or 13 digits longs
    title = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(100), nullable=False)
    date_of_death = db.Column(db.String(100))
    