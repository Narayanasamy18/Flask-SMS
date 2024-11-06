from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student_register'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)