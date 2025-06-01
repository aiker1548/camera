from enum import Enum as PyEnum


class TimeOfDay(PyEnum):
    MORNING = "Утро"
    DAY = "День"
    EVENING = "Вечер"
    NIGHT = "Ночь"

class TracingStatus(PyEnum):
    DONE = "Done"
    RUN = "Run"
    ERROR = "Error"