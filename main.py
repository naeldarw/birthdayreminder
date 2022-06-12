from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def hello():
    lottery_numbers = random.sample(range(1, 50), 6)
    name = 'Nael'
    return render_template('hello.html', name=name, lottery_numbers=lottery_numbers)


