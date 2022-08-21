# birthdayreminder

## Flask documentation
https://flask.palletsprojects.com/en/2.1.x/

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

