# birthdayreminder

## Flask documentation
- https://flask.palletsprojects.com/en/2.1.x/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/

## Start it locally

To run it locally, first we have to set the environment variable FLASK_APP.
Then we can start the server with the 'flask' command
```shell script
set FLASK_APP=main
flask run --host=0.0.0.0

```
We have to restart this every time we change the website

## Apply the changes on git
```shell script
git add .
git commit -m "test"
git push
```

This will update the github repository, and also trigger a new deployment on Heroku.

## Bootstrap
Bootstraps: https://getbootstrap.com/docs/4.0/components/navbar/

## Flask-Alchemy
https://pythonbasics.org/flask-sqlalchemy/


## Inspect database wih this tool
https://sqlitebrowser.org/

- Download SQLite Browser and Install
- Start Flask Application by running main.py (which will create an db.sqlite3 file)
- Start SQLite Browser, Click open database, navigate to the location of your project and open the db.sqlite3 file

## CRUD application

app.route(web address) is above every functions in main.py. It represents the web adress.

-C for create(POST): when someone posts Data on the website input field(html),
with href you redirect to a function that deals with the data through request.form(dictionary with the data entered).
The keys of request.form are the names of your html input fields.

-R for read(GET)
-U for update: what the update function does if someone POSTS data:
    elif request.method == "POST":
        data = request.form
        person.update(data)
        return redirect(url_for("birthday_reminder"))
-D for delete: We hold a dictionary of every "person", if we want to delete for instance Nael's entry
we delete Nael's dictionary.


## IaaS / PaaS / SaaS

### IaaS (2-4 EUR/month)
Infrastructure as a Service

When we order IaaS, we get:
- Server without any software on it (physical server or VM, running linux)
- Just a database, and connection details to the database

Example:
https://www.hetzner.com/

What we have to provide:
- Server Setup, DB Setup, Application Code, Monitoring, ...

### PaaS (30 EUR/month)
Platform as a Service

When we order PaaS, we get:
- Server
- Possible Database
- Preinstalled Software, that can run our application
- Deployment scripts, functions that we can use to deploy
- some logging and monitoring to start and stop the application
- possibly: Integration with git

Example:
https://www.heroku.com/

What we have to provide:
- Application Code, that can be run by the PaaS

### SaaS
Software as a Service

When we order SaaS, we get:
- Server
- Application which is started

What we have to provide:
- Just go on the Website and use it
- Just use the API that is given by the application

Example:
- Birthday Reminder
- https://play.google.com/store/apps/details?id=com.ornior.energy.finder

How to make money with your SaaS project


SQL Code:

SELECT * 
FROM Participants 
WHERE Participants.Vegetarian='Vegetarian';


SELECT * 
FROM Artist
WHERE Artist.Name='Aerosmith';


SELECT ArtistId, Name
FROM Artist
WHERE Artist.Name='Aerosmith';


SELECT ArtistId, Name
FROM Artist
WHERE Artist.Name LIKE 'A%';


SELECT *
FROM Invoice
WHERE Invoice.BillingCountry='USA' AND Invoice.Total>15;


Select DISTINCT BillingCountry
FROM Invoice;


Select max(total)
FROM Invoice;


SELECT  DISTINCT Title
FROM Album 
WHERE Album.ArtistId = '1' ;

SELECT Album.Title, Artist.Name
FROM Album
INNER JOIN Artist ON Album.ArtistId = Artist.ArtistId ;


SELECT Album.Title, Artist.Name
FROM Album
INNER JOIN Artist ON Album.ArtistId = Artist.ArtistId ;

C:\Code\github.com\naeldarw

FLASK MIGRATION INFORMATION:
https://flask-migrate.readthedocs.io/en/latest/index.html
!!! Make sure to: set FLASK_APP=main.py

Many-to-one relationship:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships

**FLASK MIGRATE:**

-Flak Migrate is a package that allows us to upgrade our database's version. For instance, 
if we want to add an "email" column, we make the necessary changes in the python, and then we use
Flask Migrate to add an "email" column to the database, without creating a scratch data base(we keep our previous data).

-First, we write migrate = Migrate(app, db, render_as_batch=True) in the python, to connect the app to our database.
Then, with "flask db init", on the terminal, we create a "migrations" repository. After adding the python code
for the "email column", we make flask db migrate -m "Initial migration.", on the terminal to initialize the change.
On the "versions" repository from migrations, we'll see our initial python file with an upgrade function and a downgrade function.
We make "flask db upgrade", on the terminal to upgrade the change.(We will see a new "email" column in our database.)

-TO RESUME the terminal commands: 1. flask db migrate -m "Initial migration."
2. "flask db upgrade" and to create the migrations repository: "flask db init"

IMPLEMENTATION OF MANY TO ONE(ONE USER AND MANY "PERSONS" CLASSES, that have birthdays):
-Our "User" class will have a global variable "persons": persons = db.relationship('Persons', backref='user', lazy=True,
will connect to the 'Persons' class, which will have a foreign key: user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False),
so each time a user will add a person's birthday, it will be added to the database, and will have
a "user_id" column, which is user.id, so the person's id. And we'll be able to access all the person's birthdays
the user has added through Persons.user_id.

COOKIES:
-We use cookies to who is the user (that is registered) is using the app, or if he needs to register.
-Only one cookie at a time, on the same browser.(the last one sent.)
-After one day, the cookie is deleted, the data stays, so when the user logs
in again, he finds back his data. One day after the login time, the user needs to 
log in again.


**PATRICK SQLITE EXERCISES**:
- Ex2: 
SELECT BillingCity, COUNT(InvoiceId)
FROM Invoice
GROUP BY BillingCity
ORDER BY COUNT(InvoiceId) DESC;
- Ex3: 
SELECT COUNT(Track.TrackId)
FROM Track
WHERE Track.MediaTypeId = '5';
- Ex4:
SELECT Artist.Name, COUNT(Album.ArtistId)
FROM Artist
INNER JOIN Album ON Album.ArtistId = Artist.ArtistId
GROUP BY Artist.Name
ORDER BY COUNT(Album.ArtistId) DESC;
- Ex5:
SELECT Track.GenreId, COUNT(Track.TrackId)
FROM Track
GROUP BY Track.GenreId
ORDER BY COUNT(Track.TrackId) DESC;
- Ex6:
SELECT Invoice.CustomerId, Invoice.Total
FROM Invoice
ORDER BY Invoice.Total DESC;
