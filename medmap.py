import json
import os

from dbhelper import DBHelper
from flask import Flask, send_from_directory
from flask import render_template
from flask import request

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    print('home')
    foods = DB.get_all_foods()
    foods = json.dumps(foods)
    return render_template("home.html", foods=foods)

// Just for the Icon on browser
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

# @app.route("/add", methods=["POST"])
# def add():
#     try:
#         data = request.form.get("description")
#         DB.add_input(data)
#     except Exception as e:
#         print(e)
#         print('B')
#     return home()

@app.route("/saveitem", methods=['POST'])
def save_item():
    print('saveitem')
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_food(category,
                 date,
                 latitude,
                 longitude,
                 description)
    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()

   
if __name__ == '__main__':
    app.run(port=5000, debug=True)
from datetime import datetime

import pymysql
import dbconf


class DBHelper:

    def connect(self, database="db_pinfood"):
        return pymysql.connect(host='localhost',
                               user=dbconf.dbuser,
                               passwd=dbconf.dbpassword,
                               db=database)

    def get_all_foods(self):
        connection = self.connect()
        try:
            query = "SELECT latitude, " \
                    "longitude, " \
                    "date, " \
                    "category, " \
                    "description FROM foods;"

            with connection.cursor() as cursor:
                cursor.execute(query)

            named_foods = []

            for food in cursor:
                named_food = {
                    'latitude': food[0],
                    'longitude': food[1],
                    'date': datetime.strftime(food[2], '%Y- %m-%d'),
                    'category': food[3],
                    'description': food[4]
                }

                named_foods.append(named_food)

            return named_foods

        finally:
            connection.close()

    def add_food(self, category, date, latitude, longitude, description):
        connection = self.connect()

        try:
            query = "INSERT INTO foods (" \
                    "category, " \
                    "date, " \
                    "latitude, " \
                    "longitude, " \
                    "description) \
                    VALUES (%s, %s, %s, %s, %s)"

            with connection.cursor() as cursor:
                cursor.execute(query,
                               (category,
                                date,
                                latitude,
                                longitude,
                                description))
                connection.commit()

        except Exception as e:
            print(e)

        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()

        try:
            query = "DELETE FROM foods;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()
