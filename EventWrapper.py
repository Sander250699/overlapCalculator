class Event:
    def __init__(self, start, end, availability, person):
        self.start = start
        self.end = end
        self.availability = availability
        self.person = person

    def print_event(self):
        print(f'Start: {self.start}, end: {self.end}, availability: {self.availability}')

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_person(self):
        return self.person.get_name()

    def get_availability(self):
        return self.availability

    def set_start(self, x):
        self.start = x


class AvailabilityEvent:
    def __init__(self, start, end, available_persons):
        self.start = start
        self.end = end
        self.available_persons = available_persons

    def print_event(self):
        print(f'Start: {self.start}, end: {self.end}, with {self.available_persons}')

    def get_available_persons(self):
        return self.available_persons

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end
