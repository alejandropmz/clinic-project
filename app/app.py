from flask import Flask, render_template, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

mysql = MySQL(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "clinic"


@app.route("/")
def index():
    return redirect(url_for("pacientes"))


@app.route("/pacientes")
def pacientes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pacientes")
    patients = cursor.fetchall()
    cursor.close()

    # appointments
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM citas")
    appointments = cursor.fetchall()
    cursor.close()
    print(appointments)
    return render_template(
        "patients.html", patients=patients, appointments=appointments
    )


""" citas """


@app.route("/citas")
def citas():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    
    """
    )
    all_data = cursor.fetchall()
    cursor.close()
    return render_template("appointments.html", appointments=all_data)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
