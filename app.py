
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import Flask, session, request, redirect, render_template, flash, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from jinja2 import Environment
from login import login_required

import random

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])

# configure app
app = Flask(__name__)
jinja_env.add_extension('jinja2.ext.loopcontrols')
# templates auto reload
app.config["TEMPLATES_AUTO_RELOADED"] = True

# configure session
app.config["SESSION_PERMANENT"] = True # For Extra Security
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'db'}

# configure SQLAlchemy for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'My national secret'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
engine = create_engine("sqlite:///database.db")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=True)

class Student(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    guardian = db.Column(db.String(50), nullable=False)
    guardian_contact = db.Column(db.String(50), nullable=True)
    teacher_id = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return '<Student %r>' % self.name

class Teacher(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cell = db.Column(db.Integer, nullable=False)
    id_card = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Teacher %r>' % self.name

db.create_all()


# global variable
variable = 0


def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def loggedin():
    try:
        if session["user_id"]:
            return True
        if session["school"]:
            return True
    except KeyError:
        return False


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["Allow"] = "POST"
    return response

# security
@app.route("/login", methods=["GET", "POST"])
def login():
    if loggedin():
        session.clear()
        return redirect("/login")
    else:
        if request.method == "POST":
            username = request.form.get("username")
            if not username:
                flash("missing username")
                return redirect("/login")

            password = request.form.get("password")
            if not password:
                flash("missing password")
                return redirect("/login")

            user = User.query.filter_by(username=username).first()
            if not user:
                flash("username not found")
                return redirect("/login")

            if not check_password_hash(user.hash, password):
                flash("Incorrect password")
                return redirect("/login")

            user = User.query.filter_by(username=username).first()
            session["user_id"] = user.id
            return redirect("/")
        elif request.method == "GET":
            return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username or len(username) < 5:
            flash("Invalid Username. Username must at least be 5 characters long")
            return redirect("/register")
        
        password = request.form.get("password")
        if not password or len(password) < 8:
            flash("Invalid Password. Password must be at least 8 characters long")
            return redirect("/register")

        confirmation = request.form.get("confirmation")
        if not confirmation or confirmation != password:
            flash("Confirmation password does not match password")
            return redirect("/register")

        hash = generate_password_hash(password)

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists")
            return redirect("/register")

        new_user = User(username=username, hash=hash)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully. Please log in.")
        return redirect("/login")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear
    return redirect("/login")


"--------------------------------------------------------------"

# routes
"""""""""
@app.route("/school", methods=["POST"])
def school():
    session["school"] = request.form.get("schoolname")
    return redirect("/")
"""""""""

def rem_tmp():
    if os.path.exists("tmp.db"):
        os.remove("tmp.db")

# home
@app.route("/")
@login_required
def index():
    rem_tmp()
    data = {
        "students": Student.query.filter_by(user_id=session["user_id"]).count(),
        "teachers": Teacher.query.filter_by(user_id=session["user_id"]).count(),
        "courses": Student.query.filter_by(user_id=session["user_id"]).group_by("course").count(),
        "males": Student.query.filter_by(user_id=session["user_id"], gender="Male").count(),
        "females": Student.query.filter_by(user_id=session["user_id"], gender="Female").count(),
        "fee": engine.execute("select sum(fee) as sum_1 from student where user_id = ?", session["user_id"]).fetchall(),
        "salary": engine.execute("select sum(salary) as sum_1 from teacher where user_id = ?", session["user_id"]).fetchall()
    }
    if data["students"] < 1:
        data["fee"] = 0
    else:
        data["fee"] = data["fee"][0].sum_1
    if data["teachers"] < 1:
        data["salary"] = 0
    else:
        data["salary"] = data["salary"][0].sum_1
    return render_template("index.html", data=data)

# add
def reds(page):
    if "student" in page:
        if "edit" in page:
            return "/students"
    if "teacher" in page:
        if "edit" in page:
            return "/teachers"
    return "/add"

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    rem_tmp()
    if request.method == "POST":
        form = request.form.get("submit")
        id = request.form.get("id")
        name = request.form.get("name")
        if not name:
            flash("Perhaps You fogot to enter the name")
            return redirect(reds(form))
        age = request.form.get("age")
        if not age or not isint(age) or int(age) < 1:
            flash("Invalid age. Minimum 1")
            return redirect(reds(form))
        gender = request.form.get("gender")
        if not gender or gender not in ["Male", "Female", "Other"]:
            flash("Invalid Gender")
            return redirect(reds(form))
        if "student" in request.form.get("submit"):
            course = request.form.get("course")
            if not course:
                flash("You fogot to enter the course")
                return redirect(reds(form))
            fee = request.form.get("fee")
            if not fee or not isint(fee) or int(fee) < 0:
                flash("Invalid Fee. Minimum 0")
                return redirect(reds(form))
            guardian = request.form.get("guardian")
            if not guardian:
                flash("Missing guardian")
                return redirect(reds(form))
            guardian_contact = request.form.get("g_contact")
            if not guardian_contact:
                flash("Missing guardian contact")
                return redirect(reds(form))
            country = request.form.get("country")
            if not country:
                flash("Missing country")
                return redirect(reds(form))
            teacher_id = request.form.get("teacher_id")
            if not teacher_id:
                teacher_id = ""
            if "edit" in request.form.get("submit"):
                row = engine.execute("select * from Student where user_id = ? and id = ?", session["user_id"], id).fetchall()
                print(len(row))
                if len(row) < 1:
                    flash("Student not found. Try refreshing the page")
                    return redirect("/students")
                engine.execute("update Student set name = ?, age = ?, gender = ?, course = ?, fee = ?, guardian = ?, guardian_contact = ?, country = ?,teacher_id = ? where user_id = ? and id = ?", name, age, gender, course, fee, guardian, guardian_contact, country, teacher_id, session["user_id"], id)
                flash("updated successfully")
                return redirect("/students")
            student = Student(user_id=session["user_id"], name=name, age=age, gender=gender, course=course, fee=fee, guardian=guardian, guardian_contact=guardian_contact, country=country, teacher_id=teacher_id)

            db.session.add(student)
            db.session.commit()
            flash("Student added successfully")
            
        elif "teacher" in request.form.get("submit"):
            # validate
            cell = request.form.get("cell")
            if not cell or not isint(cell):
                flash("Invalid cell")
                return redirect(reds(form))
            id_card = request.form.get("id_card")
            if not id_card or not isint(id_card):
                flash("Invalid NIC")
                return redirect(reds(form))
            salary = request.form.get("salary")
            if not salary or not isint(salary) or int(salary) < 0:
                flash("Invalid Salary")
                return redirect(reds(form))
            # update if edit
            if "edit" in request.form.get("submit"):
                row = engine.execute("select * from Teacher where user_id = ? and id = ?", session["user_id"], id).fetchall()
                print(len(row))
                if len(row) < 1:
                    flash("Teacher not found. Try refreshing the page")
                    return redirect("/teachers")
                engine.execute("update Teacher set name = ?, age = ?, gender = ?, cell = ?, id_card = ?, salary = ? where user_id = ? and id = ?", name, age, gender, cell, id_card, salary, session["user_id"], id)
                flash("updated successfully")
                return redirect("/teachers")
            # add to database
            teacher = Teacher(user_id=session["user_id"], name=name, age=age, gender=gender, cell=cell, id_card=id_card, salary=salary)
            db.session.add(teacher)
            db.session.commit()
            flash("Teacher added successfully")
            
        return redirect(reds(form))
    teachers = Teacher.query.filter_by(user_id=session["user_id"]).all()
    return render_template("add.html", teachers=teachers)

@app.route("/students")
@login_required
def students():
    rem_tmp()
    students = Student.query.filter_by(user_id=session["user_id"]).all()
    teachers = Teacher.query.filter_by(user_id=session["user_id"]).all()
    return render_template("students.html", students=students, teachers=teachers)

@app.route("/teachers")
@login_required
def teachers():
    rem_tmp()
    teachers = Teacher.query.filter_by(user_id=session["user_id"]).all()
    return render_template("teachers.html", teachers=teachers)


@app.route("/delete", methods=["GET","POST"])
@login_required
def delete():
    rem_tmp()
    page = request.args.get("page")
    id = request.args.get("id")
    if "student" in page:
        student = engine.execute("delete from Student where user_id = ? and id = ?", session["user_id"], id)
        flash("Deleted successfully")
        return redirect("/students")
    elif "teacher" in page:
        teacher = engine.execute("delete from Teacher where user_id = ? and id = ?", session["user_id"], id)
        flash("Deleted successfully")
        return redirect("/teachers")

@app.route("/export", methods=["POST", "GET"])
@login_required
def export():
    if request.method == "POST":
        students = Student.query.filter_by(user_id=session["user_id"])
        teachers = Teacher.query.filter_by(user_id=session["user_id"])
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp.db"
        db.create_all()
        engine1 = create_engine("sqlite:///tmp.db")
        engine1.execute("drop table if exists user")
        for student in students:
            engine1.execute("insert into student values(?,?,?,?,?,?,?,?,?,?,?)", 0, student.id, student.name, student.age, student.gender, student.course, student.fee, student.country, student.guardian, student.guardian_contact, student.teacher_id)
        for teacher in teachers:
            engine1.execute("insert into teacher values(?,?,?,?,?,?,?,?)", 0, teacher.id, teacher.name, teacher.gender, teacher.age, teacher.cell, teacher.id_card, teacher.salary)

        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        return send_file('tmp.db', attachment_filename='student-database.db')
    flash("Export: method not allowed")
    return redirect("/")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_id():
    ids = Teacher.query.filter(1==1)
    fids = Teacher.query.filter_by(user_id=session["user_id"]).count()
    iids = list()
    for sid in ids:
        iids.append(sid.id)
    if len(iids) < 1:
        bigg = 1
    else:
        bigg = max(iids)

    if fids < 1:
        fids = 4
    while True:
        flag = False
        id = random.randint(bigg, bigg + fids)
        for ID in ids:
            if id == ID.id:
                flag = True
                break
        if flag == False:
            return id
        bigg = bigg + fids

@app.route("/imports", methods=["GET", "POST"])
@login_required
def imports():
    rem_tmp()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                if filename == 'database.db':
                    filename = 'sdatabase.db'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                engine2 = create_engine("sqlite:///" + filename)
                students = engine2.execute("select * from student")
                teachers = engine2.execute("select * from teacher")
                tids = list()
                for teacher in teachers:
                    tids.append(teacher.id)
                    ID = random_id()
                    tids.append(ID)
                    t = Teacher(user_id=session["user_id"], id=ID, name=teacher.name, age=teacher.age, gender=teacher.gender, id_card=teacher.id_card, cell=teacher.cell, salary=teacher.salary)
                    db.session.add(t)
                    db.session.commit()
                for student in students:
                    for i in range(len(tids)):
                        if tids[i] == student.teacher_id:
                            ID = tids[i + 1]
                    s = Student(user_id=session["user_id"], name=student.name, age=student.age, gender=student.gender, fee=student.fee, course=student.course, country=student.country, guardian=student.guardian, guardian_contact=student.guardian_contact, teacher_id=ID)
                    db.session.add(s)
                    db.session.commit()
                
                flash("Data imported successfully")
                os.remove(filename)
                return redirect("/")
            except KeyError:
                flash("Something bad happened.Database must contain Student and Teacher table with specified entities. Make sure to only import the database exported from this app")
                return redirect("/")
        else:
            flash("file not accessible")
            return redirect("/")
    return '''
    <!doctype html>
    <a href=/ > Home </a>
    <title>Import</title>
    <h1>Import database</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
if __name__ == "__main__":
    app.run()





