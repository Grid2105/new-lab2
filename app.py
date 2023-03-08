from flask import Flask, render_template, request
import pymysql
import pandas as pd

app = Flask(__name__)


def connect():
    ENDPOINT = "db-for-lab2.mysql.database.azure.com"
    PORT = 3306
    USER = "admin2023"
    PASSWORD = "3202-nimda"
    DBNAME = "new_database"

    return pymysql.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME,
                           ssl_key="DigiCertGlobalRootCA.crt.pem")


@app.route("/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        operation = request.form.get("string")
        try:

            res = str(eval(operation))
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO operations (operation, result) VALUES ('{operation}', '{res}');")

            connection.commit()
            cursor.close()
            connection.close()

            return render_template("index.html", result=operation + " = " + res)
        except:
            return render_template("index.html", result="error")

    return render_template("index.html", result="")


@app.route("/show", methods=["GET", "POST"])
def show_history():
    connection = connect()
    result = pd.read_sql("SELECT * FROM operations", con=connection)
    connection.close()
    return result.to_html()


if __name__ == "__main__":
    app.run()
