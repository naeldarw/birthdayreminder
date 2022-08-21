from main import Persons


def get_person_by_id(person_id: int, persons: list[Persons]) -> Persons:
    for person in persons:
        if person["id"] == person_id:
            return person

