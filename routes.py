from flask import render_template, request, redirect, url_for, flash
from models import db, Student
from werkzeug.utils import secure_filename
from datetime import datetime
import os

def register_routes(app):
    @app.route('/')
    def index():
        students = Student.query.all()
        return render_template('index.html', students=students)

    @app.route('/add', methods=['GET', 'POST'])
    def add_student():
        if request.method == 'POST':
            try:
                photo = request.files['photo']
                if photo:
                    filename = secure_filename(photo.filename)
                    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    photo.save(photo_path)
                    photo_path = photo_path.replace('static/', '')
                else:
                    photo_path = None

                student = Student(
                    f_name=request.form['f_name'],
                    l_name=request.form['l_name'],
                    course=request.form['course'],
                    subject=request.form['subject'],
                    year=request.form['year'],
                    age=int(request.form['age']),
                    gender=request.form['gender'],
                    birth=datetime.strptime(request.form['birth'], '%Y-%m-%d'),
                    contact=request.form['contact'],
                    email=request.form['email'],
                    photo=photo_path,
                    reg_no=request.form['reg_no']
                )
                db.session.add(student)
                db.session.commit()
                flash('Student added successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
                return redirect(url_for('add_student'))
        return render_template('add.html')

    @app.route('/edit/<reg_no>', methods=['GET', 'POST'])
    def edit_student(reg_no):
        student = Student.query.filter_by(reg_no=reg_no).first_or_404()
        if request.method == 'POST':
            try:
                student.f_name = request.form['f_name']
                student.l_name = request.form['l_name']
                student.course = request.form['course']
                student.subject = request.form['subject']
                student.year = request.form['year']
                student.age = int(request.form['age'])
                student.gender = request.form['gender']
                student.birth = datetime.strptime(request.form['birth'], '%Y-%m-%d')
                student.contact = request.form['contact']
                student.email = request.form['email']
                
                photo = request.files['photo']
                if photo:
                    filename = secure_filename(photo.filename)
                    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    photo.save(photo_path)
                    student.photo = photo_path.replace('static/', '')

                db.session.commit()
                flash('Student updated successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        return render_template('edit.html', student=student)

    @app.route('/delete/<reg_no>')
    def delete_student(reg_no):
        student = Student.query.filter_by(reg_no=reg_no).first_or_404()
        try:
            if student.photo:
                photo_path = os.path.join('static', student.photo)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
            db.session.delete(student)
            db.session.commit()
            flash('Student deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))