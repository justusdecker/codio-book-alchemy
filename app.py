from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Book, Author
from copy import deepcopy
app = Flask(__name__)

# OperationError fix
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'library.sqlite')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite' 

class AsSortWorkAround:
    """
    The sorting works correctly at first:
    
        sorted_books = sorted(zip(books, author_names),key=lambda x: x[1].lower())
    
    - (<Book 4>, 'Anika Decker') 4
    - (<Book 5>, 'Justus Decker') 5
    - (<Book 1>, 'Martin Luther') 1
    - (<Book 3>, 'Ralf König') 3
    - (<Book 2>, 'Tommy Jaud') 2
    
    This gives me the same problem:
    
        books = Book.query.select_from(Book, Author).order_by(Author.name.lower()).all()
    
    The list breaks in the next line(idk how to fix so here is a workaround):
    
        sec_books = [book[0] for book in sorted_books] #unsorted why?
    
    - <Book 4> Vollidiot Tommy Jaud 1 4
    - <Book 5> Zitronenröllchen Ralf König 2 5
    - <Book 1> ImABook Martin Luther 0 1
    - <Book 3> Zwei vernünftige Erwachsene, die sich mal nackt gesehen haben Anika Decker 3 3
    - <Book 2> Why am i doing this 3AM in the morning? Justus Decker 4 2
    """

db.init_app(app)
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    books = Book.query.all()
    authors = Author.query.all()
    if request.method == 'POST':
        sorting_method = request.form['sorting_method']
        if sorting_method == 'title':
            sec_books = sorted(books,key=lambda x: x.title)
        if sorting_method == 'author':
            author_names = [author.name for author in authors]

            books = [
                {
                    'title': book.title,
                    'isbn': book.isbn, 
                    'publication_year': book.publication_year,
                    'author_id':book.author_id,
                    'author': author_names[book.author_id-1]
                    } for book in books]
            
            books = sorted(books,key=lambda x: x['author'])

            sec_books = [AsSortWorkAround() for attrs in books]
            
            # Sets the same attributes as Book + author
            for idx,wa in enumerate(sec_books):
                for attr in books[idx]:
                    if attr == 'author': continue # removing it because we dont it twice
                    wa.__setattr__(attr,books[idx][attr])
    return render_template('home.html', books=sec_books,authors = authors)


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