from flask import Flask, jsonify, request, render_template
import psycopg2
from credentials import DBNAME, USER, PASSWORD, HOST, PORT

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/departments')
def get_departments():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DBNAME, 
        user=USER, 
        password=PASSWORD, 
        host=HOST, 
        port=PORT
    )
    cur = conn.cursor()

    # Query to get departments sorted by total spend
    cur.execute("""
        SELECT agency_name, SUM(value_aud) AS total_spend
        FROM contracts
        GROUP BY agency_name
        ORDER BY total_spend DESC
    """)
    departments = [{'name': row[0], 'total_spend': row[1]} for row in cur.fetchall()]

    # Close the connection
    cur.close()
    conn.close()

    # Return data as JSON
    return jsonify(departments)

@app.route('/data')
def get_data():
    # Get the department from the query string
    department = request.args.get('department')

    # Connect to the database
    conn = psycopg2.connect(
        dbname=DBNAME, 
        user=USER, 
        password=PASSWORD, 
        host=HOST, 
        port=PORT
    )
    cur = conn.cursor()

    # Query to get the top 5 categories for the selected department
    cur.execute("""
        SELECT category_name, SUM(value_aud) AS total_spending
        FROM contracts
        WHERE agency_name = %s
        GROUP BY category_name
        ORDER BY total_spending DESC
        LIMIT 5
    """, (department,))
    
    rows = cur.fetchall()

    # Prepare data as a list of dictionaries (for JSON)
    data = [{'category': row[0], 'total': row[1]} for row in rows]

    # Close the connection
    cur.close()
    conn.close()

    # Return data as JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)