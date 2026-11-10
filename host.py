from action import add_action_to_db, ActionData
from deliverable import add_deliverable_to_db, DeliverableData
from db_api import make_sql_query
import datetime
import io
from flask import Flask, jsonify, request, render_template, abort, send_file
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


@app.route('/actions')
def view_rap():
        return render_template('view.html')

@app.route('/reports')
def export_rep():
        return render_template('reports.html')

@app.route('/api/export/csv')
def export_csv():
        """
                Exports the data as comma-seperated values. 

                Returns: The downloaded file containing the CSV

                Paramaters: None
        """

        csv_export_name = 'RAP_CSV.csv'

        # Schema for the CSV
        csv_content = 'Pillar,Action,DeliverableID,DeliverableName,DeliverableDesc,DeliverableStart,DeliverableDue,Assigned,Comments\r\n'

        # Dynamically generate the contents of the csv
        rows = make_sql_query("SELECT * FROM deliverables")
        for row in rows:
                action_id = int(row[6])
                action_name = make_sql_query("SELECT name FROM actions WHERE id = ? LIMIT 1", str(action_id))[0][0]

                pillar_table = {
                        1 : "Relationships",
                        2 : "Respect",
                        3 : "Opportunities",
                        4 : "Governance",
                }
                pillar = pillar_table[make_sql_query("SELECT pillar FROM actions WHERE id = ? LIMIT 1", str(action_id))[0][0]]

                deliverable_id = int(row[0])
                deliverable_name = row[1]
                deliverable_desc = row[2]
                deliverable_start = row[4]
                deliverable_due = row[5]
                assigned = make_sql_query("SELECT username FROM login WHERE id = ? LIMIT 1", str(row[3]))[0][0]

                comment_arr = make_sql_query("SELECT text FROM comments WHERE deliverables_id = ?", str(deliverable_id))
                comment_str = ",".join(comment_arr)

                csv_line = ','.join([pillar, action_name, str(deliverable_id), 
                        deliverable_name, deliverable_desc, str(deliverable_start), 
                        str(deliverable_due), assigned, comment_str])

                csv_content += csv_line + '\r\n'

        file_buffer = io.BytesIO(csv_content.encode('utf-8'))
        file_buffer.seek(0)

        return send_file(
                file_buffer,
                mimetype='text/csv',
                as_attachment=True,
                download_name=csv_export_name
        )

@app.route('/api/export/report')
def export_report():
    report_name = 'RAP_report.md'
    
    pillar_table = {
        1: "Relationships",
        2: "Respect",
        3: "Opportunities",
        4: "Governance",
    }

    deliverables_query = """
        SELECT 
            d.id, 
            d.name, 
            d.description, 
            d.start_date, 
            d.due_date, 
            a.name AS action_name, 
            a.pillar AS pillar_id, 
            l.username AS assigned_user
        FROM deliverables d
        LEFT JOIN actions a ON d.action_id = a.id
        LEFT JOIN login l ON d.assigned_id = l.id
        ORDER BY a.pillar, a.name, d.id
    """
    
    deliverables = make_sql_query(deliverables_query)

    markdown_lines = ["# Reconciliation Action Plan (RAP) Report\n"]

    for row in deliverables:
        d_id, d_name, d_desc, d_start, d_due, action_name, pillar_id, assigned_user = row
        
        pillar_name = pillar_table.get(pillar_id, "Unknown Pillar")
        
        # Format the start and due dates into strings
        
        # Build deliverable section
        markdown_lines.append(f"## {d_name}")
        markdown_lines.append(f"**Pillar:** {pillar_name}  ")
        markdown_lines.append(f"**Action:** {action_name or 'N/A'}  ")
        markdown_lines.append(f"**Assigned To:** {assigned_user or 'Unassigned'}  ")
        markdown_lines.append(f"**Timeline:** {d_start} to {d_due}\n")
        markdown_lines.append(f"### Description\n{d_desc}\n")

        # Fetch comments
        comments = make_sql_query("SELECT text FROM comments WHERE deliverables_id = ?", str(d_id))
        
        markdown_lines.append("### Comments")
        if comments:
            for comment in comments:
                markdown_lines.append(f"> {comment[0]}")
        else:
            markdown_lines.append("_No comments available._")

        markdown_lines.append("\n---\n")

    report_content = "\n".join(markdown_lines)

    file_buffer = io.BytesIO(report_content.encode('utf-8'))
    file_buffer.seek(0)

    return send_file(
        file_buffer,
        mimetype='text/markdown',
        as_attachment=True,
        download_name=report_name,
    )
    
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
