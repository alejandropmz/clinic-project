from flask import Flask, render_template, redirect, url_for, request, jsonify
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


@app.route("/pacientes/<int:id>")
def detalle_paciente(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
    patient = cursor.fetchall()
    cursor.close()
    return render_template("patient-detail.html", patient=patient[0])


@app.route("/editar_paciente/<int:id>")
def editar_paciente(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
    patient = cursor.fetchall()
    cursor.close()
    return render_template("edit-patient.html", patient=patient[0])


@app.route("/guardar_edicion_paciente/<int:id>", methods=["POST"])
def guardar_edicion_paciente(id):
    ident = request.form["id"]
    first_names = request.form["first-names"]
    last_names = request.form["last-names"]
    birth_date = request.form["birth-date"]
    contact = request.form["contact"]
    email = request.form["email"]
    address = request.form["address"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    UPDATE pacientes
    SET identificacion = %s,
    nombres = %s,
    apellidos = %s,
    nacimiento = %s,
    contacto = %s,
    correo = %s,
    direccion = %s
    WHERE id = %s
    """,
        (ident, first_names, last_names, birth_date, contact, email, address, id),
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("detalle_paciente", id=id))


@app.route("/crear_paciente", methods=["GET", "POST"])
def crear_paciente():
    if request.method == "GET":
        return render_template("create-patient.html")
    ident = request.form["id"]
    first_names = request.form["first-names"]
    last_names = request.form["last-names"]
    birth_date = request.form["birth-date"]
    contact = request.form["contact"]
    email = request.form["email"]
    address = request.form["address"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    INSERT INTO pacientes
    (identificacion, nombres, apellidos, nacimiento, contacto, correo, direccion)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
        (ident, first_names, last_names, birth_date, contact, email, address),
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("pacientes"))


@app.route("/eliminar_paciente/<int:id>")
def eliminar_paciente(id):
    cursor = mysql.connection.cursor()
    # patient appointments
    cursor.execute("DELETE FROM citas WHERE paciente = %s", (id,))
    cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("pacientes"))


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


@app.route("/citas/<int:id>")
def detalle_cita(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos, pacientes.contacto, pacientes.correo
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    WHERE citas.id = %s
    """,
        (id,),
    )
    appointment = cursor.fetchall()
    cursor.close()
    return render_template("appointment-detail.html", appointment=appointment[0])


@app.route("/editar_cita/<int:id>")
def editar_cita(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos, pacientes.contacto, pacientes.correo
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    WHERE citas.id = %s
    """,
        (id,),
    )
    appointment = cursor.fetchall()
    cursor.close()
    return render_template("edit-appointment.html", appointment=appointment[0])


@app.route("/guardar_edicion_cita/<int:id>", methods=["POST"])
def guardar_edicion_cita(id):
    date = request.form["date"]
    start = request.form["start"]
    end = request.form["end"]
    reason = request.form["reason"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    UPDATE citas
    SET fecha = %s,
    ingreso = %s,
    salida = %s,
    razon = %s
    WHERE id = %s
    """,
        (date, start, end, reason, id),
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("detalle_cita", id=id))


@app.route("/crear_cita", methods=["GET", "POST"])
def crear_cita():
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pacientes")
        patients = cursor.fetchall()
        cursor.close()
        return render_template("create-appointment.html", patients=patients)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pacientes")
    patient = cursor.fetchall()
    cursor.close()
    date = request.form["date"]
    start = request.form["start"]
    end = request.form["end"]
    reason = request.form["reason"]
    patient = request.form["patient"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    INSERT INTO citas
    (fecha, ingreso, salida, razon, paciente, estado)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (date, start, end, reason, patient, 1),
    )
    mysql.connection.commit()

    cursor.execute("""
    SELECT pacientes.*, citas.fecha, citas.ingreso, citas.salida, citas.razon
    FROM pacientes
    JOIN citas
    ON pacientes.id = citas.paciente
    WHERE pacientes.id = %s
    """, (patient))
    patient_info = cursor.fetchall()
    cursor.close()
    print(patient_info)
    return render_template("create-bill.html", patient=patient_info[0])


""" 
A ESTE ENDPOINT LE FALTA LA FECHA Y LAS HORAS DE ENTRADA Y SALIDA
DE LA CONSULTA PARA PODER VINCULAR EL PAGO UNICO A LA CONSULTA
PRIMERO AÑADIR ESTOS CAMPOS AL FORMULARIO DE LA FACTURA
 """

@app.route("/eliminar_cita/<int:id>")
def eliminar_cita(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE citas SET estado = %s WHERE id = %s",
        (
            2,
            id,
        ),
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("citas"))


@app.route("/paciente_citas/<int:paciente_id>")
def paciente_citas(paciente_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos, pacientes.contacto, pacientes.correo
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    WHERE citas.paciente = %s
    """,
        (paciente_id,),
    )
    all_data = cursor.fetchall()
    cursor.close()
    return render_template("patient-appointment-list.html", data=all_data)


""" Facturas """


@app.route("/facturas")
def facturas():
    return render_template("bills.html")


@app.route("/crear_factura")
def crear_factura():
    return render_template("create-bill.html")


@app.route("/guardar_factura", methods=["POST"])
def guardar_factura():
    data = dict(request.form.items())
    print(data)
    ## buscar paciente por id
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id FROM pacientes WHERE identificacion = %s", (data["client-id"])
    )
    patient_id = cursor.fetchone()[0]

    cursor.execute(
        """
    INSERT INTO pagos (valor, descripcion)
    VALUES (%s, %s)
    """,
        (data["appointment-cost"], data["appointment-description"]),
    )

    cursor.execute(
        """
    SELECT id FROM citas WHERE paciente = %s, AND cita
    """
    )

    cursor.execute
    return jsonify({"redirect_url": "facturas"})


if __name__ == "__main__":
    app.run(debug=True, port=4000)
