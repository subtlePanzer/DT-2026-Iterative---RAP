from db_api import make_sql_query_return_index

class ActionData:
        action_id: int
        pillar: int
        name: str
        description: str
        deliverable_ids: list[int] # list of int ids

        def __init__(self, action_id: int, pillar: int, name: str, description: str, deliverable_ids: list[int]):
                self.action_id = action_id
                self.name = name
                self.description = description
                self.deliverable_ids = deliverable_ids
                self.pillar = pillar


def add_action_to_db(data: ActionData):
        return make_sql_query_return_index('''
                INSERT INTO actions (name, description, pillar)
                VALUES (?, ?, ?)
        ''', (data.name, data.description, data.pillar))
