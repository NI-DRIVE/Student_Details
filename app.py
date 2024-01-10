from flask import Flask, render_template, request, redirect, abort
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['INITIALIZED'] = False  # Added initialization flag
db.init_app(app)

@app.before_request
def before_request():
    if not app.config['INITIALIZED']:
        app.config['INITIALIZED'] = True
        with app.app_context():
            db.create_all()

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        hobby = request.form.getlist('hobbies')
        hobbies = ",".join(map(str, hobby))

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']
        country = request.form['country']

        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')

@app.route('/')
def retrieve_list():
    students = StudentModel.query.all()
    return render_template('datalist.html', students=students)

@app.route('/<int:id>')
def retrieve_student(id):
    student = StudentModel.query.get(id)
    if student:
        return render_template('data.html', student=student)
    return f"Student with id = {id} does not exist"

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.get(id)

    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()

        hobby = request.form.getlist('hobbies')
        hobbies = ",".join(map(str, hobby))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']
        country = request.form['country']

        updated_student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(updated_student)
        db.session.commit()
        return redirect('/')
    
    return render_template('update.html', student=student)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    student = StudentModel.query.get(id)
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)


