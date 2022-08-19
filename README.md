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
