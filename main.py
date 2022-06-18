from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route("/")
def hello():
    lottery_numbers = random.sample(range(1, 50), 6)
    name = 'Nael'
    return render_template('hello.html', name=name, lottery_numbers=lottery_numbers)

@app.route("/advent_of_code")
def advent_of_code():
    return 'advent_of_code'

@app.route("/advent_of_code/<int:day>")
def advent_of_code_day(day):
    return f"Today is {day}."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
