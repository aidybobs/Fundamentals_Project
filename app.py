from flask import Flask, render_template
from os import getenv
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('secretkey')


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
    shifts = db.relationship('Shift', secondary=Rota, backref='shiftbr')


class Shifts(db.Model):
    __tablename__ = 'Shifts'
    shift_no = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    no_emps = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    emps = db.relationship('Employee', secondary=Rota, backref='empbr')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
