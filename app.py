# imports
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

# importing the configs
from config.configs import Config,DevelopmentConfig,ProductionConfig

# init flask
app = Flask(__name__)

# setting the app to use to development config
app.config.from_object(DevelopmentConfig)

# SQLALCHEMY
db = SQLAlchemy(app)

# models
from models.department import DepartmentModel
from models.employees import EmployeeModel


@app.before_first_request
def create_tables():
    # db.drop_all()
    db.create_all()

# home route
@app.route('/')
def home():
    return render_template('homepage.html')

# departments route
@app.route('/departments', methods=['GET','POST'])
def departments():

    # fetching all departments and store them in a variable called all_my_depts
    all_my_depts = DepartmentModel.fetch_all_departments()

    # flash(type(all_my_depts))

    # for x in all_my_depts:
    #     flash(x.name)

    if request.method == 'POST':
        # fetch the user's input from the modal/form
        dept = request.form['department']

        # check if a department alread exists
        if DepartmentModel.check_dept_exist(dept):
            # if true warn the user it already exists
            flash('Department Already Exists, 'Danger')
        else:
            # if it is false, add the record to the database

            record = DepartmentModel(name=dept)
            record.create()
            flash('success')
            return redirect(url_for('departments'))

    return render_template('departments.html', madepts=all_my_depts)


@app.route('/department/employees/<int:id>', methods=['GET','POST'])
def department_employees(id):

    dpt_emp = DepartmentModel.fetch_by_id(id)

    employees = dpt_emp.employee



    return render_template('departmentemp.html', wafanyakazi=employees,
                           dep=dpt_emp)

# employees
@app.route('/employees', methods=['GET','POST'])
def employees():

    all_my_depts = DepartmentModel.fetch_all_departments()

    allemps = EmployeeModel.fetch_all()
    # flash(type(allemps))

    if request.method == 'POST':
        name = request.form['fullname']
        gender = request.form['gender']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        department = request.form['department']
        idnumber = request.form['idnumber']
        krapin = request.form['krapin']
        basicsalary = request.form['basicsalary']
        benefits = request.form['benefits']

        if EmployeeModel.check_idnumber_exists(idnumber):
            flash('already exists')
            return redirect(url_for('employees'))
        else:
            emp = EmployeeModel(fullname=name,gender=gender,email=email,phonenumber=phonenumber,idnumber=idnumber,
                                department=department,krapin=krapin,basicsalary=basicsalary,benefits=benefits)

            emp.create_record()

            flash('success')

            return redirect(url_for('employees'))

    return render_template('employees.html', madepts=all_my_depts, employees= allemps)

@app.route('/employee/edit/<int:id>', methods=['POST'])
def edit_employees(id):
    if request.method == 'POST':
        name = request.form['fullname']
        gender = request.form['gender']
        email = request.form['email']
        phonenumber = request.form['phonnumber']
        department = request.form['department']
        idnumber = request.form['idnumber']
        krapin = request.form['krapin']
        basicsalary = request.form['basicsalary']
        benefits = request.form['benefits']

        update = EmployeeModel.edit_employee_by_id(id=id,name=name,gender=gender,
                                                   email=email,phone=phone,
                                                   idnumber=idnumber,kra=krapin,basicsalary=basicsalary,
                                                   benefits=benefits)

        if update:
            flash('update successful')
            return redirect(url_for('employees'))
        else:
            flash('record not found')
            return redirect(url_for('employees'))

@app.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    delete = EmployeeModel.delete_by_id(id)

    try:
        if delete:
            flash('Successfully deleted')
            return redirect(url_for('employees'))
    except Exception as e :
        flash('Unable to delete record at this this time')


if __name__ == '__main__':
    app.run(debug=True)