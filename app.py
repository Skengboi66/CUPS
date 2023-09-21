from flask import  render_template, url_for, request, redirect
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
db = SQLAlchemy(app)

class User(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    university_supervisor = db.Column(db.String(100), nullable=False)
    company_supervisor = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.company}', '{self.university_supervisor}', '{self.company_supervisor}')"
    
class CompanySupervisor(db.Model):
    supervisor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    student = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"CompanySupervisor('{self.name}', '{self.email}', '{self.student}')"
    
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.student_id'), nullable=False)
    quality_of_work = db.Column(db.Integer)
    communication_skills = db.Column(db.Integer)
    punctuality = db.Column(db.Integer)
    teamwork = db.Column(db.Integer)
    problem_solving = db.Column(db.Integer)



@app.before_first_request
def create_tables():
    db.create_all()


#page routing 
@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/feedback')
def feedback():
    return render_template('studentFeedback.html') 

@app.route('/companysupervisorlogin')
def company_supervisor_login():
    return render_template('companySupervisorLogin.html')

@app.route('/addCompanySupervisor')
def add_CompanySupervisor():
    return render_template('addCompanySupervisor.html')

@app.route('/student')
def student():
    return render_template('studentHome.html')

@app.route('/supervisor')
def supervisor():
    return render_template('supervisorHome.html')  
 
@app.route('/admin')
def admin():
    return render_template('adminHome.html')

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    error_message = None  # Initialize error_message
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

@app.route('/addAccount', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company = request.form['company']
        university_supervisor = request.form['university_supervisor']
        company_supervisor = request.form['company_supervisor']

        new_user = User(
            name=name,
            email=email,
            company=company,
            university_supervisor=university_supervisor,
            company_supervisor=company_supervisor
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('registration.html')

@app.route('/addStudent', methods=['GET', 'POST'])
def add_student():
    error_message = None  # Initialize error_message
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            company = request.form['company']
            university_supervisor = request.form['university_supervisor']
            company_supervisor = request.form['company_supervisor']

            new_user = User(
                name=name,
                email=email,
                company=company,
                university_supervisor=university_supervisor,
                company_supervisor=company_supervisor
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('admin'))
        except Exception as e:
            error_message = str(e)

    return render_template('adminHome.html', error_message=error_message)

@app.route('/deleteAccount/<int:user_id>', methods=['GET', 'POST'])
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Handle deletion here (e.g., delete the user from the database)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('view_users'))

    return render_template('deleteAccount.html', user=user)

@app.route('/provide_feedback/<int:user_id>', methods=['GET', 'POST'])
def provide_feedback(user_id):
    student = User.query.get_or_404(user_id)

    if request.method == 'POST':
        feedback_text = request.form['feedback']

        # Create a Feedback object and associate it with the student
        feedback = Feedback(
            student_id=user_id,
            quality_of_work=int(request.form.get('quality_of_work')),
            communication_skills=int(request.form.get('communication_skills')),
            punctuality=int(request.form.get('punctuality')),
            teamwork=int(request.form.get('teamwork')),
            problem_solving=int(request.form.get('problem_solving'))
        )

        db.session.add(feedback)
        db.session.commit()

        # Redirect to the student's profile page or any other appropriate page
        return redirect(url_for('supervisor', user_id=user_id))

    return render_template('supervisorHome.html', student=student)

@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('userList.html', users=users)

    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)