from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


app = Flask (__name__)

#database connectivity
db = SQLAlchemy(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://database.db'

#secret key for session
app.config['SECRET_KEY']= 'thisisasecretkey'

#Database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, Primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)


#page routing 
@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)