from action import add_action_to_db, ActionData
import datetime
from deliverable import add_deliverable_to_db, DeliverableData
from db_api import make_sql_query
from flask import Flask, jsonify, request, render_template
from person import Person

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
        return render_template('action.html')

@app.route('/actions')
def view_rap():
        return render_template('view.html')

def pull_users():
        outs = make_sql_query('''
                SELECT username, id FROM login
        ''')

        users = [{"id": out[1], "name": out[0]} for out in outs]
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

@app.route('/api/get_pillar', methods=['GET'])
def get_pillar():
    try:
        # Get the pillar ID from the query string parameters (?pillar=X)
        pillar = request.args.get('pillar', type=int)
        
        if pillar is None:
            return jsonify({"error": "Pillar parameter is required"}), 400

        actions_rows = make_sql_query("SELECT id, name FROM actions WHERE pillar = ?", (pillar,))
        data = []

        for action_id, action_name in actions_rows:
            deliverables_rows = make_sql_query(
                "SELECT name FROM deliverables WHERE action_id = ?", 
                (action_id,)
            )

            # DEBUG: Print to your terminal console to see if SQLite finds anything
            print(f"Action ID {action_id} deliverables from DB: {deliverables_rows}")

            if deliverables_rows:
                # Force extract the string from each row tuple safely
                subrows = [str(row[0]) for row in deliverables_rows if row]

                data.append({
                    "id": action_id,
                    "action_name": action_name,
                    "main_data": "Assigned", 
                    "subrows": subrows
                })
            else:
                data.append({
                    "id": action_id,
                    "action_name": action_name,
                    "main_data": "No deliverable assigned",
                    "subrows": []
                })

        return jsonify(data)

    except Exception as e:
        print(f"Error in get_pillar: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/submit', methods=['POST'])
def handle_submit():
        item_names = request.form.getlist('itemName[]')
        user_ids = request.form.getlist('userId[]')
        pillar = request.form.getlist('pillar[]')

        action_id = add_action_to_db(ActionData(0, 1, request.form['title'], request.form['description'], [])) # pass in other data

        print(f"{action_id=}")


        for name, user_id in zip(item_names, user_ids):
                print(f"Item: {name}, Assigned User ID: {user_id}")
                add_deliverable_to_db(DeliverableData(0, name, "", Person.get_person_by_id(user_id), datetime.datetime(2000, 1, 2), datetime.datetime(2000, 1, 2), [], action_id)) # pass in other data

        return "Form submitted successfully!"
