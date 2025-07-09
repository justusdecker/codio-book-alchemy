from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Book, Author

app = Flask(__name__)

# OperationError fix
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'library.sqlite')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite' 



db.init_app(app)
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    #sorted(books,key=)
    return render_template('home.html', books=books,authors = Author.query.all())


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']
        new_author = Author(name = name, birth_date = birth_date, date_of_death = date_of_death)
        db.session.add(new_author)
        db.session.commit()
        return redirect('/')
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        
        title = request.form['title']
        author = int(request.form['author'].split('_')[1])
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        new_book = Book(title=title, author_id=author, publication_year=publication_year,isbn=isbn)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/')
    return render_template('add_book.html',authors=Author.query.all())

if __name__ == '__main__':

    app.run(debug=True)
    pass