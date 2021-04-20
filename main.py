import sys
from src import util


if __name__ == '__main__':
    events = util.load_ics()
    if not events:
        print("Laden schlug fehl, Programm wird beendet!")
        sys.exit()

    [start_date, end_date] = util.get_start_end_date()
    #[start_date, end_date] = [datetime.date(2021, 4, 1), datetime.date(2021, 4, 15)]

    events = util.filter_dates(events, start_date, end_date)
    text = util.generate_text(events)
    print(text)
    util.save(text)

