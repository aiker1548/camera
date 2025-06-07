from enum import Enum as PyEnum


class TimeOfDay(str, PyEnum):
    MORNING = "MORNING"
    DAY = "DAY"
    EVENING = "EVENING"
    NIGHT = "NIGHT"
    
class TracingStatus(str, PyEnum):
    DONE = "DONE"
    RUN = "RUN"
    ERROR = "ERROR"


