# Allows time and dates
from datetime import datetime

# Allows access paths on our file system
import os

from flask import redirect

# Import Flask
from flask import Flask
from flask import render_template
from flask import request

# Flask's version of SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

''' 
    Figured out where our project path is and set up a database file
    with its full path and the sqlite:/// prefix to tell SQLAlchemy 
    which database engine we're using.
'''

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

# Initialize flask app, passing __name__ variable to lef Flask configure other parts of our app.
app = Flask(__name__) 

# Tell web app where database will be stored
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



# Initialize connection to database with db variable
db = SQLAlchemy(app)

''' 
    Create a new class which inherits from a basic database model,
    provided by SQLAlchemy. This makes SQLAlchemy create a table called book
    which store our Book objects.
'''
class Book(db.Model):
    ''' 
        Create an attribute of our book called title. SQLAlchemy uses
        this as a column name in our book table. Title consist of a String
        of at most 80 characters, that should never store two or more books
        with the same title (book titles should be unique ), every book needs to have a title
        (the title isn't nullable ), and the title is the main way that we identify 
        a specific book in our database (title is the primary_key)
    '''
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=True)
    publisher = db.Column(db.String(80), unique=False, nullable=True)
    date = db.Column(db.String(80), unique=False, nullable=True)
    '''
        Define how to represent our book object as a string. This
        allows us to do things like print(book) and see meaningful
        output
    '''
    def __repr__(self):
        return "<Title: {}>".format(self.title) #and "<Author: {}>".format(self.author)

# Maps app(/) to the home() function
@app.route("/", methods=["GET", "POST"])

# Define a function and returns a static string. This displays when we visit the page.
def home():
    books = None
    # authors = None
    # check if someone just submitted the form and if so access the data through the request.form variable.
    if request.form:
        try:
            ''' Grab the "title" input from the form and use it to initialize
                a new Book object. We save this new Book to a variable named
                book.
            '''
            book = Book(title=request.form.get("title"), author=request.form.get("author"),publisher=request.form.get("publisher"), date=request.form.get("date"))
            # Add the book to our database and commit our changes to persist them
            db.session.add(book)
            #db.session.add(author)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Failed to add book")
            print(e)
    
            #print(request.form)
    # Get all of the current books out of the database
    books = Book.query.all()
    #authors = Book.query.all()
    return render_template("home.html", books=books)

''' Gets the old and updated title
    Fetches the book with the old title from the database
    Updates that book's title to the new title
    Saves the book to the database
    Redirects the user to the main page
'''
# Maps app(/update) to the update() function
@app.route("/update", methods=["POST"])

def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    #author = Author.query.filter_by()
    book.title = newtitle
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

# Ensure web servers don't start if we ever import this script into another one.
if __name__ == "__main__":
    app.run(debug=True)

