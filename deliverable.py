import datetime
from db_api import make_sql_query
from person import Person

class DeliverableData:
        deliverable_id: int
        name: str
        description: str
        assigned: Person
        due: datetime.datetime
        started: datetime.datetime
        comment_ids: list[int] # list of int ids
        action_id: int

        def __init__(self, deliverable_id: str, name: str, description: str, assigned: Person, due: datetime.datetime, started: datetime.datetime, comment_ids: list[int], action_id: int):
                self.name = name
                self.description = description
                self.assigned = assigned
                self.started = started
                self.due = due
                self.comment_ids = comment_ids
                self.action_id = action_id

def add_deliverable_to_db(data: DeliverableData):
        print(data.action_id)

        make_sql_query('''
                INSERT INTO deliverables (name, description, assigned_id, start_date, due_date, action_id)
                VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.name, data.description, data.assigned.db_id, data.started.timestamp(), data.due.timestamp(), data.action_id))
