import os
import util.sorting
import datetime

from flask_migrate import Migrate

from flask import Flask, render_template, request, redirect, url_for, make_response

import uuid
import itertools
import random
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail, Message

app = Flask(__name__)

# EMAIL SETTINGS
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'birthdayreminder321@gmail.com'
app.config['MAIL_PASSWORD'] = 'Birthday123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# APP, COOKIE AND DB SETTINGS
LOGIN_COOKIE_KEY = 'BIRTHDAY-REMINDER-LOGIN-TOKEN'
MAX_COOKIE_LOGIN_VALIDITY = datetime.timedelta(days=1)

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3").replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

counter = itertools.count()

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    login_token = db.Column(db.String(200), nullable=True)
    last_login_time = db.Column(db.DateTime(), nullable=True)
    persons = db.relationship('Persons', backref='user', lazy=True)

    def __init__(self, email, name, session_token, login_time):
        self.name = name
        self.email = email
        self.login_token = session_token
        self.last_login_time = login_time


class Persons(db.Model):
    id = db.Column('person_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    name = db.Column(db.String(100))
    birthday = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, email, name, birthday, hobby):
        self.name = name
        self.birthday = birthday
        self.hobby = hobby
        self.email = email

    def __repr__(self):
        return f"Persons({self.name}, {self.birthday}, {self.hobby}, {self.email})"


# db.create_all()


class Website:
    def __init__(self):
        self.images = []
        self.name = ""
        self.persons = []

        self.tasks_completed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


website = Website()


@app.route("/", methods=["GET"])
def hello():
    lottery_numbers = random.sample(range(1, 50), 6)
    website.name = 'Nael'
    website.images = [
        ('Kebab', "https://carlsbadcravings.com/wp-content/uploads/2020/07/Doner-Kebabs-v14-500x500.jpg"),
        ('Subway',
         "https://www.qsrmagazine.com/sites/default/files/styles/story_page/public/2022-01/subwaybajaturkeyavocado.jpg?itok=FMXyS1Re"),
        ('Burger',
         "data:image/jpeg;base64,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"),
        ('Salad',
         "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2014/09/Mandarin-Chicken-Salad-8.jpg"),
        ('Spaghetti',
         "https://assets.bonappetit.com/photos/5a2826911a178d3636ce8fdf/4:5/w_2583,h_3229,c_limit/seafood-spaghetti-with-mussels-and-shrimp.jpg")

    ]
    return render_template('hello.html', name=website.name, lottery_numbers=lottery_numbers, images=website.images)


@app.route("/advent_of_code")
def advent_of_code():
    return render_template("advent_of_code.html", tasks=website.tasks_completed)


@app.route("/advent_of_code/<int:day>")
def advent_of_code_day(day):
    return f"Today is {day}."


@app.route("/birthday_reminder")
def birthday_reminder():
    # TODO: @Nael: return the list in a sorted way, and not just all elements we know

    cookie_login_token = request.cookies.get(LOGIN_COOKIE_KEY)
    _1day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    user = User.query.filter(User.login_token == cookie_login_token).filter(User.last_login_time > _1day_ago).first()
    # if login is expired, send the user back to register
    if not user:
        return redirect(url_for("register"))

    # if user is logged in, get the users persons to be listed
    persons = list(user.persons)
    curr_date = datetime.date.today()
    persons = util.sorting.sort_persons_by_upcoming_birthday(persons, curr_date.strftime('%Y-%m-%d'))
    return render_template("birthdayreminder.html", username=user.name, persons=persons)


@app.route("/persons/<int:person_id>/edit", methods=["GET", "POST"])
def update_person_data(person_id):
    person = Persons.query.get(person_id)
    if request.method == "GET":
        if person is None:
            return redirect(url_for("birthday_reminder"))
        else:
            return render_template("edit.html", person=person)
    elif request.method == "POST":
        data = request.form
        person.name = data["name"]
        person.hobby = data["hobby"]
        person.birthday = data["birthday"]
        db.session.add(person)
        db.session.commit()
        return redirect(url_for("birthday_reminder"))


@app.route("/delete_birthday/<int:person_id>")
def delete_birthday(person_id: int):
    person = Persons.query.get(person_id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for("birthday_reminder"))


@app.route("/register", methods=["GET", "POST"])
def register():
    # https://pythonbasics.org/flask-cookies/
    if request.method == "POST":
        dic = request.form

        session_token = str(uuid.uuid4())
        login_time = datetime.datetime.now()

        user = User.query.filter(User.name == dic["name"]).first()
        if not user:
            db.session.add(User(dic["name"], session_token, login_time))
            db.session.commit()
        else:
            user.login_token = session_token
            user.login_time = login_time
            db.session.add(user)
            db.session.commit()

        resp = make_response(redirect(url_for("birthday_reminder")))
        resp.set_cookie(
            LOGIN_COOKIE_KEY,
            session_token,
            max_age=MAX_COOKIE_LOGIN_VALIDITY,
            expires=login_time + MAX_COOKIE_LOGIN_VALIDITY
        )

        return resp

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/api/birthdays", methods=["POST"])
def add_birthday():
    dic = request.form

    cookie_login_token = request.cookies.get(LOGIN_COOKIE_KEY)
    _1day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    user = User.query.filter(User.login_token == cookie_login_token).filter(User.last_login_time > _1day_ago).first()
    # if login is expired, send the user back to register
    if not user:
        return redirect(url_for("register"))

    if dic["name"] != "":
        new_person = Persons(dic["email"], dic["name"], dic["birthday"], dic["hobby"])
        new_person.user_id = user.id

        db.session.add(new_person)
        db.session.commit()

    return redirect(url_for("birthday_reminder"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
