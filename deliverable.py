from person import Person
import datetime

class DeliverableData:
        id: int
        name: str
        description: str
        assigned: Person
        due: datetime.datetime
        started: datetime.datetime
        comment_ids: list[int] # list of int ids
        action_id: int

def add_deliverable_to_db(data: DeliverableData):
        make_sql_query('''
                INSERT INTO deliverables (name, description, assigned_id, start_date, due_date, action_id)
                VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.name, data.description, data.assigned.db_id, data.started.timestamp(), data.due.timestamp(), data.action_id))
