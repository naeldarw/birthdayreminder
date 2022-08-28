from typing import List
import datetime
from main import Persons


def days_left(birthdate: str, current_date: str) -> int:
    # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    year = current_date[0:4]
    FORMAT = "%Y-%m-%d"
    birthdate_obj = datetime.datetime.strptime(birthdate, FORMAT)
    curr_date_obj = datetime.datetime.strptime(current_date, FORMAT)
    birthdate_obj = birthdate_obj.replace(year=curr_date_obj.year)
    difference = birthdate_obj - curr_date_obj
    if difference.days < 0:
        birthdate_obj = birthdate_obj.replace(year=curr_date_obj.year + 1)
        difference = birthdate_obj - curr_date_obj
    return difference.days




def sort_persons_by_upcoming_birthday(persons: List[Persons], current_date: str) -> List[Persons]:
    """Sort the persons by the number of days needed to reach their birthday,

    :param persons:
    :type persons: list
    :return: return a list of sorted persons whose birthday is next
    :rtype: list
    """
    #[].sort(...)
    #new_list = sorted([], ...)
    # TODO: @Nael: Sort the list of persons correctly
    persons.sort(key=lambda x: days_left(x.birthday, current_date))

    return persons


# TODO: BONUS: also get the number of days left until the next birthdays
