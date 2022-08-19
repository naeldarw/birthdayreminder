

def get_person_by_id(person_id, persons):
    for person in persons:
        if person["id"] == person_id:
            return person

