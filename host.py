from action import add_action_to_db, ActionData
from db_api import make_sql_query
from flask import Flask, jsonify, request, render_template, abort
import datetime

app = Flask(__name__)

def launch():
        # launch the website
        app.run(debug=True)

@app.route('/')
def index_page():
        # homepage
        return render_template('index.html')

@app.route('/action/new')
def add_new_action():
        return render_template('new_action.html')

@app.route('/action/<int:action_id>')
def action_detail(action_id):
        action_row = make_sql_query(
                'SELECT id, name, description FROM actions WHERE id = ?',
                (action_id,)
        )

        if not action_row:
                abort(404)

        action = action_row[0]
        deliverables = make_sql_query('''
                SELECT d.id, d.name, d.due_date, l.username
                FROM deliverables d
                LEFT JOIN login l ON l.id = d.assigned_id
                WHERE d.action_id = ?
        ''', (action_id,))

        deliverable_items = []
        for item in deliverables:
                due_date = 'TBD'
                if item[2]:
                        try:
                                due_date = datetime.datetime.fromtimestamp(item[2]).strftime('%Y-%m-%d')
                        except Exception:
                                due_date = str(item[2])

                deliverable_items.append({
                        'id': item[0],
                        'responsibility': item[3] or 'Unassigned',
                        'timeline': due_date,
                        'deliverable': item[1]
                })

        data = {
                'pillar': 'RAP Alignment',
                'pillar_description': action[2] or 'Action details and status',
                'action_title': action[1],
                'deliverables': deliverable_items
        }

        return render_template('action.html', data=data)

@app.route('/deliverable/<int:del_id>')
def deliverable_detail(del_id):
        deliverable = make_sql_query(
                'SELECT d.name, d.description, d.due_date, l.username FROM deliverables d LEFT JOIN login l ON l.id = d.assigned_id WHERE d.id = ?',
                (del_id,)
        )

        if not deliverable:
                abort(404)

        item = deliverable[0]
        due_date = 'TBD'
        if item[2]:
                try:
                        due_date = datetime.datetime.fromtimestamp(item[2]).strftime('%Y-%m-%d')
                except Exception:
                        due_date = str(item[2])

        details = {
                'name': item[0],
                'description': item[1],
                'assigned': item[3] or 'Unassigned',
                'due_date': due_date
        }

        return render_template('deliverable_detail.html', deliverable=details)


def pull_users():
        outs = make_sql_query('''
                SELECT username, id FROM login
        ''')

        users = [{"id": out[0], "name": out[1]} for out in outs]
        return users

@app.route('/api/users', methods=['GET'])
def get_users():
        try:
                try:
                        users_data = pull_users()
                except Exception as e:
                        print(e)

                return jsonify(users_data)
        except Exception as e:
                return jsonify({"error": str(e)}), 500



@app.route('/submit', methods=['POST'])
def handle_submit():
        item_names = request.form.getlist('itemName[]')
        user_ids = request.form.getlist('userId[]')
        add_action_to_db(ActionData(0, request.form['title'], request.form['description'], []))
        # TODO: add deliverables to the deliverable table

        for name, user_id in zip(item_names, user_ids):
                print(f"Item: {name}, Assigned User ID: {user_id}")

        return "Form submitted successfully!"
