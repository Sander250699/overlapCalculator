from EventWrapper import *
from PersonsWrapper import *
from datetime import datetime
from random import *
import argparse
import csv

limit = 100
add_value = 5
persons = 2


def generate_name():
    random_string = ''

    for _ in range(5):
        # Considering only upper and lowercase letters
        random_integer = randint(97, 97 + 26 - 1)
        flip_bit = randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    return random_string


def create_events(number_of_persons):
    event_list = []
    end_times = []
    start_times = []
    all_created = []
    persons = []
    for x in range(number_of_persons):
        start_times.append(1)
        end_times.append(2)
        event_list.append([])
        all_created.append(False)
        persons.append(Person(generate_name()))

    while all_created.count(True) != len(all_created):
        for x in range(number_of_persons):
            if end_times[x] < limit:
                end_time = uniform(start_times[x], limit)
                if end_time == start_times[x]:
                    end_time = end_time + 1
                if end_time + add_value > limit:
                    end_time = limit
                    all_created[x] = True
                end_times[x] = end_time
                event = Event(start_times[x], end_time, bool(getrandbits(1)), persons[x])
                start_times[x] = end_time + 1
                event_list[x].append(event)
    return event_list


def handle_current_events(events, number_of_persons, next_event):
    global current_event
    current_end = limit + 1
    available_persons = []
    person = 0
    for x in range(number_of_persons):
        if next_event is not None and events[x] is not None:
            events[x].start = next_event.get_end()
        if events[x] is not None and current_end >= events[x].get_end():
            current_event = events[x]
            current_end = events[x].get_end()
            person = x
        if events[x] is not None and events[x].get_availability():
            available_persons.append(events[x].get_person())
    return current_event, person, available_persons

def calculate_overlap(events, number_of_persons):
    result_list = []
    current_events = [x[0] for x in events]
    next_event = None
    while current_events.count(None) != len(current_events):
        result = handle_current_events(current_events, number_of_persons, next_event)
        person_list = events[result[1]]
        if person_list:
            person_list.pop(0)
        if not person_list:
            # Empty list
            current_events[result[1]] = None
        else:
            current_events[result[1]] = person_list[0]
            next_event = result[0]
        if len(result_list) >= 1:
            availability_event = AvailabilityEvent(result_list[len(result_list) - 1].get_end(), result[0].get_end(),
                                                   result[2])
        else:
            availability_event = AvailabilityEvent(result[0].get_start(), result[0].get_end(), result[2])
        result_list.append(availability_event)
        if result[0].get_end() == limit:
            break
    return result_list


def get_events(number_of_persons):
    person1 = Person('Sander')
    person2 = Person('Emma')
    event_list = []
    list_1 = []
    list_2 = []
    list_1.append(Event(1, 5, True, person1))
    list_1.append(Event(5, 7, False, person1))
    list_1.append(Event(7, 15, False, person1))
    list_1.append(Event(15, 20, True, person1))
    list_2.append(Event(1, 2, True, person2))
    list_2.append(Event(2, 7, True, person2))
    list_2.append(Event(7, 12, False, person2))
    list_2.append(Event(12, 20, False, person2))
    event_list.append(list_1)
    event_list.append(list_2)
    return event_list


def calculate_number_of_slots(events):
    count = 0
    for event_list in events:
        count = count + len(event_list)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate overlap.')
    parser.add_argument('persons', metavar='p', default=5, type=int, help='How many persons do you want')
    parser.add_argument('limit', metavar='l', default=10, type=int, help='end hour (in integer format)')
    args = parser.parse_args()
    persons = args.persons
    limit = args.limit
    event_lists = create_events(persons)
    # event_lists = get_events(persons)
    number_slots = calculate_number_of_slots(event_lists)
    start = datetime.now()
    overlap_list = calculate_overlap(event_lists, persons)
    end = datetime.now()
    start_time = start.strftime("%H:%M:%S")
    end_time = end.strftime("%H:%M:%S")
    print('Number of persons = ', persons)
    print('Number of slots= ', number_slots)
    print("Start time =", start_time)
    print("End ime =", end_time)
    fields = ["Start", "End", "Availability"]
    with open('availability.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(fields)
        for x in overlap_list:
            filewriter.writerow([x.get_start(), x.get_end(), x.get_available_persons()])
