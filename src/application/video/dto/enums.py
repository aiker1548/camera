from enum import Enum as PyEnum


class TimeOfDay(PyEnum):
    MORNING = "MORNING"
    DAY = "DAY"
    EVENING = "EVENING"
    NIGHT = "NIGHT"
    
class TracingStatus(PyEnum):
    DONE = "DONE"
    RUN = "RUN"
    ERROR = "ERROR"