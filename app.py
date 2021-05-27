import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.secret_key = "My Secret Key"

DB_HOST = os.getenv('DB_HOST') 
DB_PASS = os.getenv('DB_PASS') 
DB_NAME = os.getenv('DB_NAME') 
DB_USER = os.getenv('DB_USER') 

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50))
    lName = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    isDeleted = db.Column(db.Boolean())

    def __init__(self, fName, lName, email, mobile, isDeleted):
        self.fName = fName
        self.lName = lName
        self.email = email
        self.mobile = mobile
        self.isDeleted = isDeleted


@app.route('/')
def homepage():
    try:
        users_list = User.query.filter_by(isDeleted=False).all()
    except:
        users_list = ""

    return render_template("index.html", users=users_list)


@app.route('/adduser', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        fName = request.form['fName']
        lName = request.form['lName']
        email = request.form['email']
        mobile = request.form['mobile']
        user_data = User(fName, lName, email, mobile, False)
        try:
            db.session.add(user_data)
            db.session.commit()
        except exc.IntegrityError:
            flash("Duplicate email/phone number")
            return redirect(request.url)

        flash('Employee added successfully!')
        return redirect(url_for('homepage'))

    elif request.method == 'GET':
        return render_template('form.html')


@app.route('/updateUser', methods=['POST'])
def update_user():
    if request.method == 'POST':
        id = request.form['id']
        user_data = User.query.get(id)
        user_data.fName = request.form['fName']
        user_data.lName = request.form['lName']
        user_data.email = request.form['email']
        user_data.mobile = request.form['mobile']
        try:
            db.session.commit()
        except exc.IntegrityError:
            flash("Duplicate email/phone number")
            return redirect(url_for('homepage'))

        flash("User Updated Successfully!")
        return redirect(url_for('homepage'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_user(id):
    if request.method == 'GET':
        my_data = User.query.get(id)
        my_data.isDeleted = True;
        db.session.commit()

        flash("User Deleted")
        return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
