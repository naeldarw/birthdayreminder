import datetime


class Person(object):
    def __init__(self, name, dish, age):
        self.name = name
        self.dish = dish
        self.age = age

    def __repr__(self):
        return f"Person({self.name}, {self.dish}, {self.age})"


def get_my_dish(p):
    return p.dish


def by_age(p):
    return p.age


def main():
    my_dish = lambda p: p.dish

    me = Person("Patrick", "Ravioli", 20)
    print(my_dish(me))
    print(get_my_dish(me))
    print((lambda p: p.dish)(me))  # anonymous function, function without function name
    print((lambda p, number: p.dish + "  " + str(number))(me, 10))  # many arguments, 1 return
    print((lambda p, number: (p.dish, number))(me, 10))  # many arguments, many return

    p1 = Person("Nael", "Ravioli", 20)
    p2 = Person("Patrick", "Ravioli", 30)
    p3 = Person("Sam", "Ravioli", 40)

    people = [p1, p2, p3]
    # ascending
    people.sort(key=lambda x: x.age)
    print(people)
    # descending
    people.sort(key=lambda x: x.age, reverse=True)
    print(people)

    people.sort(key=by_age, reverse=True)
    print(people)


def dates():
    birthday1 = datetime.date(2000, 10, 30)
    # today = datetime.date.today()
    today = datetime.date(2022, 8, 28)

    birthday1 = birthday1.replace(year=today.year)

    difference = today-birthday1
    print(difference)
    print(difference.days)


def parseDates():
    my_bday = "2003-10-24"
    today_str = "2022-10-14"
    FORMAT = "%Y-%m-%d"

    my_bday_dt = datetime.datetime.strptime(my_bday, FORMAT)
    today_dt = datetime.datetime.strptime(today_str, FORMAT)

    print(my_bday_dt, type(my_bday_dt))

    difference = today_dt - my_bday_dt
    print(difference)


if __name__ == '__main__':
    # main()
    dates()
    # parseDates()
