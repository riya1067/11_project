from flask import Flask, render_template, url_for, flash, redirect, request
from forms import EntryForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
app = Flask(__name__, static_folder='static')#initialize the flask application,static folder where all static files are stored
app.config['SECRET_KEY'] = 'JhRvPw5sL8y2TkQz'#protects from cross site request forgery attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'#site.db name of the SQLite database
db = SQLAlchemy(app)#initialize the sqlalchemy database
class Post(db.Model):#defines the database model for posts
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(100), nullable=False)   
def validate_category_format(category):#validates format of the category section
    category = category.strip()  
    category = re.sub(r'\s+', ' ', category)  
    category = ' '.join(word.capitalize() for word in category.split())  
    return category
@app.route("/")#route for the main page
def mainpage():
    entries = Post.query.all()#displays all entries in the database
    category_query = request.args.get('category', '')#gets the entries with a certain category
    
    if category_query:#validates the format of the search bar input
        category_query = validate_category_format(category_query)
    
    
    
    if category_query:#filters entries to fit the format
        entries = Post.query.filter_by(category=category_query).all()
    
    return render_template('main.html', entries=entries) #redirects to main.html with all entries


@app.route("/entry/new", methods=['GET', 'POST'])#route to add a new entry
def new_post():
    form = EntryForm()#create a new instance of the entry form
    
    if form.validate_on_submit():#new isntance of Post with all data
        entry = Post(category=validate_category_format(form.category.data),
                     content=form.content.data, amount=form.amount.data)
        db.session.add(entry)
        db.session.commit()#commit changes to database
        flash('Entry successful!', 'success')#flash a success message and redirects to the main page
        return redirect(url_for('mainpage'))
    
    return render_template('entry.html', title="new entry", form=form)


if __name__ == '__main__':#run if executed directly
    app.run(debug=True)
