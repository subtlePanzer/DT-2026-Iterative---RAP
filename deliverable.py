from person import Person
import datetime

class DeliverableData:
        id: int
        assigned: Person
        due: datetime.date
        started: datetime.date
        comment_ids: list # list of int ids
