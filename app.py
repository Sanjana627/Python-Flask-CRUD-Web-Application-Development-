# Import Libraries
from flask import Flask, render_template, request,redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# create an object for flask
app = Flask(__name__)
app.secret_key = "Secret Key"


################### Database Configuration #######################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

####################################################################

#################### Model Creation ############################

class Employee(db.Model):
    __tablename__ = 'employee_data'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name=db.Column(db.String(60),index=True)
    last_name=db.Column(db.String(60),index=True)
    salary = db.Column(db.Integer)
    role=db.Column(db.String(60),index=True)

    def __init__(self, first_name,last_name,email,salary,role):
        self.first_name = first_name
        self.last_name = last_name
        self.email=email
        self.salary=salary
        self.role=role
    def __repr__(self):
        return "first_name- {} and  last_name - {} and email-{} and salary-{} and role-{} ".format(self.first_name, self.last_name,self.email,self.salary,self.role)

####################################################################
@app.before_first_request
def create_table():
    db.create_all()

#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Employee.query.all()

    return render_template("index.html", employees = all_data)





@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        salary = request.form['salary']
        role = request.form['role']
        
        
        my_data = Employee(first_name,last_name,email,salary,role)
        db.session.add(my_data)
        db.session.commit()
        flash("Employee  Details Inserted Successfully")
 
        print(first_name)
        print(last_name)
        print("details Added Successfully")
    return redirect(url_for('Index'))
 
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))

        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.email = request.form['email']
        my_data.salary = request.form['salary']
        my_data.role = request.form['role']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Details Deleted Successfully")

    return redirect(url_for('Index'))
 

if __name__=='__main__':
    app.run(debug=True)