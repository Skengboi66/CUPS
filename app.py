from flask import Flask, render_template, url_for



app = Flask (__name__)


#page routing 
@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/student')
def student():
    return render_template('studentHome.html')

@app.route('/supervisor')
def supervisor():
    return render_template('supervisorHome.html')

@app.route('/admin')
def admin():
    return render_template('adminHome.html')

@app.route('/addAccount')
def admin():
    return render_template('addAccount.html')

@app.route('/deleteAccount')
def admin():
    return render_template('deleteAccount.html')

if __name__ == '__main__':
    app.run(debug=True)