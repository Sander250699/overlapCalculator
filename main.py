from EventWrapper import *
import random

limit = 1000
add_value = 25
persons = 10


def create_events(number_of_persons):
    event_list = []
    end_times = []
    start_times = []
    all_created = []
    for x in range(number_of_persons):
        start_times.append(1)
        end_times.append(2)
        event_list.append([])
        all_created.append(False)

    while all_created.count(True) != len(all_created):
        for x in range(number_of_persons):
            if end_times[x] < limit:
                end_time = random.randint(start_times[x], limit)
                if end_time == start_times[x]:
                    end_time = end_time + 1
                if end_time + add_value > limit:
                    end_time = limit
                    all_created[x] = True
                end_times[x] = end_time
                event = Event(start_times[x], end_time, bool(random.getrandbits(1)))
                start_times[x] = end_time + 1
                event_list[x].append(event)
    return event_list


def get_event_ends_first_and_available(events, number_of_persons):
    global current_event
    current_end = limit + 1
    person = 0
    for x in range(number_of_persons):
        if events[x] is not None and current_end >= events[x].get_end():
            current_event = events[x]
            current_end = events[x].get_end()
            person = x
    return current_event, person


def calculate_overlap(events, number_of_persons):
    result_list = []
    available_persons = []
    person_list = []
    current_events = [x[0] for x in events]

    while current_events.count(None) != len(current_events):
        result = get_event_ends_first_and_available(current_events, number_of_persons)
        available_persons = []
        for x in range(number_of_persons):
            if current_events[x] is not None and current_events[x].get_availability():
                available_persons.append(x)
        if len(result_list) >= 1:
            availability_event = AvailabilityEvent(result_list[len(result_list) - 1].get_end(), result[0].get_end(),
                                                   available_persons)
        else:
            availability_event = AvailabilityEvent(result[0].get_start(), result[0].get_end(), available_persons)
        result_list.append(availability_event)
        person_list = events[result[1]]
        if result[0].get_end() == limit:
            break
        else:
            if person_list:
                person_list.pop(0)
            # add new event to list of events

            if not person_list:
                # Empty list
                current_events[result[1]] = None
            else:
                current_events[result[1]] = person_list[0]
            for event_to_change in current_events:
                if event_to_change is not None:
                    event_to_change.start = result[0].get_end()
    return result_list

def get_events(number_of_persons):
    event_list = []
    list_1 = []
    list_2 = []
    list_1.append(Event(1, 5, True))
    list_1.append(Event(5, 7, False))
    list_1.append(Event(7, 15, False))
    list_1.append(Event(15, 20, True))
    list_2.append(Event(1, 2, True))
    list_2.append(Event(2, 7, True))
    list_2.append(Event(7, 12, False))
    list_2.append(Event(12, 20, False))
    event_list.append(list_1)
    event_list.append(list_2)
    return event_list


if __name__ == '__main__':
    event_lists = create_events(persons)
   # event_lists = get_events(2)
    #for x in event_lists:
    #    for y in x:
    #        y.print_event()
    overlap_list = calculate_overlap(event_lists, persons)
    for x in overlap_list:
        x.print_event()
