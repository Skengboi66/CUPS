from flask import Flask, render_template, url_for

from flask_login import UserMixin


app = Flask (__name__)




#page routing 
@app.route('/')
def home():
    return render_template('home.html') 



if __name__ == '__main__':
    app.run(debug=True)