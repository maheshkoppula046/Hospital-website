from flask import Flask, render_template, request, redirect, url_for ,flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
import secrets
app = Flask(__name__)

import os
app.secret_key = os.urandom(24)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'  # Replace with your DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    mobile = db.Column(db.String(15), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    problem_description = db.Column(db.Text, nullable=True)
    
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()
    


# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            print("User found:", user.username)  # Debugging statement
        else:
            print("User not found")

        if user and user.password == password:
            session['user'] = user.username
            print('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            print('Invalid username or password!', 'danger')
    print("out")
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

# Registration route (optional, to add users)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        print('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
    
    
    
    
 
    

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/appointment', methods=['POST','GET'])
def appointment():
    no_of_patients = Appointment.query.all()
    count=0
    for patients in no_of_patients:
        count+=1
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobilenumber')
        doctor = request.form.get('doctor')
        date = datetime.strptime(request.form.get('date'), '%m/%d/%Y').date()
        time = datetime.strptime(request.form.get('time'), '%I:%M %p').time()
        problem_description = request.form.get('problem_description')

        new_appointment = Appointment(
            id=count,
            name=name,
            email=email,
            mobile=mobile,
            doctor=doctor,
            date=date,
            time=time,
            problem_description=problem_description
        )

        # Add to database
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('success'))
        
    return render_template('appointment.html')


@app.route('/appointments_details', methods=['POST', 'GET'])
def appointments_details():

    appointments = Appointment.query.all()
    for appointment in appointments:
        print(f"ID: {appointment.id}, Name: {appointment.name}, Date: {appointment.date}, Time: {appointment.time}, Doctor: {appointment.doctor}")
    return render_template('appointments_details.html', appointments=appointments)



@app.route('/delete_appointment', methods=['POST', 'GET'])
def delete_appointment():
    id = request.form.get('appointment_id')
    appointment_to_delete = Appointment.query.get_or_404(id)
    try:
        db.session.delete(appointment_to_delete)  
        db.session.commit() 
        return redirect(url_for('appointments_details')) 
    except Exception as e:
        db.session.rollback()  
        return f"An error occurred while trying to delete the appointment: {e}"


@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/not_fount')
def not_found():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
