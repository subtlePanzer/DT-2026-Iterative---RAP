from db_api import make_sql_query

class ActionData:
        action_id: int
        name: str
        description: str
        deliverable_ids: list[int] # list of int ids

        def __init__(self, action_id: int, name: str, description: str, deliverable_ids: list[int]):
                self.action_id = action_id
                self.name = name
                self.description = description
                self.deliverable_ids = deliverable_ids


def add_action_to_db(data: ActionData):
        make_sql_query('''
                INSERT INTO actions (name, description)
                VALUES (?, ?)
        ''', (data.name, data.description))
