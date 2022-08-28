import unittest
import util.sorting
from main import Persons


class TestPersonSorting(unittest.TestCase):
    def setUp(self) -> None:
        self.persons = [
            Persons(name="Nael", birthday="2006-06-15", hobby="Programming"),
            Persons(name="Patrick", birthday="1987-08-22", hobby="Python/Golang"),
            Persons(name="Bill Gates", birthday="1955-10-28", hobby="Microsoft"),
        ]
        # TODO: @Nael: Think of 1 more test, check if the date has the right format

    def test_sorting_by_birthday(self):
        sorted_persons = util.sorting.sort_persons_by_upcoming_birthday(self.persons)

        expected_sorted_list = [
            Persons(name="Bill Gates", birthday="1955-10-28", hobby="Microsoft"),
            Persons(name="Nael", birthday="2006-06-15", hobby="Programming"),
            Persons(name="Patrick", birthday="1987-08-22", hobby="Python/Golang"),
        ]

        self.assertEqual(
            sorted_persons, expected_sorted_list, "Expected %s, but got %s" % (
                [e.toStr() for e in expected_sorted_list],
                [e.toStr() for e in sorted_persons]
            )
        )
        #  : Expected ['Persons(Bill Gates, 1955-10-28, Microsoft)\n', 'Persons(Nael, 2006-06-15, Programming)\n', 'Persons(Patrick, 1987-08-22, Python/Golang)\n'],
        #  but got ['Persons(Nael, 2006-06-15, Programming)\n', 'Persons(Patrick, 1987-08-22, Python/Golang)\n', 'Persons(Bill Gates, 1955-10-28, Microsoft)\n']


if __name__ == '__main__':
    unittest.main()

