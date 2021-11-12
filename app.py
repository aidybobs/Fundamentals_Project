from flask import Flask, render_template, request, redirect
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField, DateField


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv("SECRET_KEY")


db = SQLAlchemy(app)


class Rota(db.Model):
    __tablename__ = 'Rota'
    id = db.Column('id', db.Integer, primary_key=True)
    emp_no = db.Column('emp_no', db.Integer, db.ForeignKey('Employees.emp_no'))
    shift_no = db.Column('shift_no', db.Integer, db.ForeignKey('Shifts.shift_no'))


class Employees(db.Model):
    __tablename__ = 'Employees'
    emp_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dept = db.Column(db.String(20), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    shifts = db.relationship('Rota', backref='shiftbr')


class Shifts(db.Model):
    __tablename__ = 'Shifts'
    shift_no = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    no_emps = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    emps = db.relationship('Rota', backref='empbr')


class EmpForm(FlaskForm):
    name = StringField("Name")
    dept = StringField("Department")
    rate = IntegerField("Pay Rate")
    hours = IntegerField("Hours")
    submit = SubmitField("Submit")


class ShiftForm(FlaskForm):
    date = DateField("Date")
    no_emps = IntegerField("No. of Employees")
    type = StringField("Type")
    hours = IntegerField("Hours")
    submit = SubmitField("Submit")


@app.route("/")
def homepage():
    rotas = Rota.query.all()
    return render_template("homepage.html", records=rotas)


@app.route("/employees")
def employees():
    employee = Employees.query.all()
    return render_template("employees.html", records=employee)


@app.route("/shifts")
def shifts():
    shift = Shifts.query.all()
    return render_template("shifts.html", records=shift)


@app.route("/editemployee/<int:emp_no>", methods=["GET", "POST"])
def editemployee(emp_no):
    form = EmpForm()
    employee = Employees.query.filter_by(emp_no=emp_no).first()
    if request.method == "POST":
        employee.name = form.name.data
        employee.dept = form.dept.data
        employee.rate = form.rate.data
        employee.hours = form.hours.data
        db.session.commit()
        return redirect("/employees")
    return render_template("editemp.html", form=form)


@app.route("/addemployee", methods=["GET", "POST"])
def addemp():
    form = EmpForm()
    if request.method == "POST":
        name = form.name.data
        dept = form.dept.data
        rate = form.rate.data
        hours = form.hours.data
        nemp = Employees(name=name, dept=dept, rate=rate, hours=hours)
        db.session.add(nemp)
        db.session.commit()
        return redirect("/employees")
    return render_template("editemp.html", form=form)


@app.route("/deleteemployee", methods=["GET", "POST"])
def delemp(emp_no):
    emp = Employees.query.filter_by(emp_no=emp_no).first()
    db.session.delete(emp)
    db.session.commit()
    return redirect("/employees")


@app.route("/addshift", methods=["GET","POST"])
def addshift():
    form = ShiftForm()
    if request.method == "POST":
        date = form.date.data
        no_emps = form.no_emps.data
        type = form.type.data
        hours = form.hours.data
        nshift = Shifts(date=date, no_emps=no_emps, type=type,hours=hours)
        db.session.add(nshift)
        db.session.commit()
        return redirect("/shifts")
    return render_template("editshift.html", form=form)


@app.route("/editshift", methods=["GET", "POST"])
def editshift():
    form = ShiftForm()
    shift = Shifts.query.filter_by(emp_no=emp_no).first()
    if request.method == "POST":
        shift.date = form.date.data
        shift.no_emps = form.no_emps.data
        shift.type = form.type.data
        shift.hours = form.hours.data
        db.session.commit()
        return redirect("/shifts")
    return render_template("editshift.html", form=form)


@app.route("/deleteshift", methods=["GET", "POST"])
def delshift(shift_no):
    shift = Shifts.query.filter_by(shift_no=shift_no).first()
    db.session.delete(shift)
    db.session.commit()
    return redirect("/employees")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
