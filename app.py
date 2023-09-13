from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    university_supervisor = db.Column(db.String(100), nullable=False)
    company_supervisor = db.Column(db.String(100), nullable=False)

#@app.route('/addAccount', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        company = request.form['company']
        university_supervisor = request.form['university_supervisor']
        company_supervisor = request.form['company_supervisor']

        new_user = User(
            id=id,
            name=name,
            email=email,
            company=company,
            university_supervisor=university_supervisor,
            company_supervisor=company_supervisor
        )
        
        

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('registration'))

    return render_template('registration.html')


app = Flask (__name__)


#page routing 
@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Check if the provided username and password match the hardcoded admin credentials
            if username == 'admin' and password == 'admin123':
                # Redirect to a dashboard or another page on successful login
                return redirect(url_for('admin'))
            else:
                error_message = "Invalid credentials. Please try again."

    return render_template('adminLogin.html', error_message=error_message if 'error_message' in locals() else '')


@app.route('/student')
def student():
    return render_template('studentHome.html')

@app.route('/supervisor')
def supervisor():
    return render_template('supervisorHome.html')  
 
@app.route('/admin')
def admin():
    return render_template('adminHome.html')

@app.route('/addCompanySupervisor')
def add_student():
    return render_template('addStudent.html')

@app.route('/addUniveristySupervisor')
def add_uniSupervisor():
    return render_template('addUniveristySupervisor.html')

@app.route('/addCompanySupervisor')
def add_CompanySupervisor():
    return render_template('addCompanySupervisor.html')

@app.route('/deleteAccount')
def delete_account():
    return render_template('deleteAccount.html')

@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('view_users'))
    return render_template('delete_user.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)