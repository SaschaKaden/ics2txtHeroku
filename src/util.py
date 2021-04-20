import easygui
from ics import Calendar
import datetime


def load_ics():
    file_type = '*.ics'
    path = easygui.fileopenbox(default=file_type, title='Laden der Kalender Datei', filetypes=file_type)
    if path is None or not path.lower().endswith('.ics'):
        print('wrong file type')
        return []

    with open(path, 'r', encoding="utf8") as file:
        cal = Calendar(file.read())
        return list(cal.events)


def get_start_end_date():
    msg = "Bitte gib Start- und Enddatum für Einträge aus. (Format: DD.MM.YYYY)"
    title = "Eingabe der Daten"
    field_names = ["Startdatum", "Enddatum"]
    field_values = easygui.multenterbox(msg, title, field_names)

    # make sure that none of the fields was left blank
    while 1:
        if field_values is None:
            break
        errmsg = ""
        for i in range(len(field_names)):
            if field_values[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % field_names[i])
        if errmsg == "":
            break  # no problems found
        field_values = easygui.multenterbox(errmsg, title, field_names, field_values)

    date_values = []
    for i in range(len(field_values)):
        day, month, year = map(int, field_values[i].split('.'))
        date_values.append(datetime.date(year, month, day))
    print("Eingabe ist:", field_values)
    return [date_values[0], date_values[1]]


def filter_dates(events, start_date, end_date):
    for x in reversed(events):
        if start_date > x.begin.datetime.date():
            events.remove(x)

    for x in reversed(events):
        if end_date < x.begin.datetime.date():
            events.remove(x)

    for i in range(len(events)):
        print(events[i].begin.datetime.date())

    return events


def str_of_day(day):
    if day == 1:
        return "Montag"
    elif day == 2:
        return "Dienstag"
    elif day == 3:
        return "Mittwoch"
    elif day == 4:
        return "Donnerstag"
    elif day == 5:
        return "Freitag"
    elif day == 6:
        return "Samstag"
    elif day == 7:
        return "Sonntag"
    else:
        return "..."


def generate_text(events):
    text = ''
    for event in events:
        if not event.name:
            continue
        date = event.begin.datetime
        title = "+++ " + str_of_day(date.weekday()) + date.strftime(", %d.%m.%Y, %H:%M Uhr: ") + event.name + " +++"
        desc = "Thema: " + event.description
        where = "Wo: " + event.location
        who = "Ansprechpartnerin: "
        text += "\n" + title + "\n" + desc + "\n" + where + "\n" + who + "\n"

    return text


def save(text):
    type = "Ergebnis.txt"
    path = easygui.filesavebox(filetypes=type, default=type, title='Speichern der Geojson Datei')
    if path is None or not path.lower().endswith(('.txt', '.geojson')):
        print('wrong file type')
        return False

    with open(path, 'w', encoding="utf8") as output_file:
        output_file.write('%s' % text)
