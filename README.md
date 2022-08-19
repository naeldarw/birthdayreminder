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

## Apply the changes
```shell script
git add .
git commit -m "test"
git push
```
Bootstraps: https://getbootstrap.com/docs/4.0/components/navbar/

## Flask-Alchemy
https://pythonbasics.org/flask-sqlalchemy/


## Inspect database wih this tool
https://sqlitebrowser.org/

- Download SQLite Browser and Install
- Start Flask Application by running main.py (which will create an db.sqlite3 file)
- Start SQLite Browser, Click open database, navigate to the location of your project and open the db.sqlite3 file
