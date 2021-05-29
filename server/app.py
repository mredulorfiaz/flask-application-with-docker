import os

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flaskext.mysql import MySQL

app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_HOST'] = os.getenv(
    'DB_HOST') if os.getenv('DB_HOST') else 'localhost'
app.config['MYSQL_DATABASE_USER'] = os.getenv(
    'DB_USER') if os.getenv('DB_USER') else 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv(
    'DB_PASS') if os.getenv('DB_PASS') else '1234'
app.config['MYSQL_DATABASE_DB'] = os.getenv(
    'DB_NAME') if os.getenv('DB_NAME') else 'flaskDB'

mysql = MySQL()
mysql.init_app(app)


@app.route('/api/v1', methods=['GET'])
def index():

    query = "SELECT * FROM flaskDB.user WHERE isDeleted=0"
    response = query_builder(query, 'select')
    users = []
    for user in response:
        users.append({
            "id": user[0],
            "fName": user[1],
            "lName": user[2],
            "email": user[3],
            "mobile": user[4]
        })

    return make_response(jsonify({
        "users": users,
        "error": False
    }))


@app.route('/api/v1/user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        json_data = request.get_json()
        try:
            f_name = json_data['fName']
            l_name = json_data['fName']
            email = json_data['email']
            mobile = json_data['mobile']
            is_deleted = 0

            query = f"INSERT INTO user (fName, lName, email, mobile, isDeleted) VALUE ('{f_name}', '{l_name}', '{email}', '{mobile}', '{is_deleted}');"
            query_builder(query, 'insert')

            return make_response(jsonify(
                error=False,
                message="Added User"
            ), 201)
        except KeyError:
            return make_response(jsonify(
                error=True,
                message="Make sure to enter all the fields!"
            ), 400)


@app.route('/api/v1/user/<id>', methods=['DELETE'])
def delete_user(id):
    query = f"SELECT * FROM user where ID = {id}"
    response = query_builder(query, 'select')

    if response:
        query = f"DELETE FROM user WHERE id = {id}"
        query_builder(query, 'delete')
        return make_response(jsonify(error=False,
                                     message="Deleted User"
                                     ), 204)
    else:
        return make_response("No such user", 200)


def query_builder(query, q_type):
    conn = mysql.connect()
    cursor = conn.cursor()
    if q_type.lower() == 'insert':
        cursor.execute(query)
        conn.commit()
    elif q_type.lower() == 'select':
        cursor.execute(query)
        return cursor.fetchall()
    elif q_type.lower() == 'delete':
        cursor.execute(query)
        conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
