from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)

mysql = MySQL(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "clinic"

app.config["SECRET_KEY"] = "my_secret_key"

""" Login """

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/")
@app.route("/pacientes")
def pacientes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE is_active = %s", (1,))
    patients = cursor.fetchall()
    cursor.close()

    # appointments
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT pacientes.id, citas.id, citas.razon, citas.estado
    FROM citas
    JOIN pacientes 
    ON pacientes.id = citas.paciente
    WHERE is_active = %s
    """,
        (1,),
    )
    appointments = cursor.fetchall()
    cursor.close()
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
    (identificacion, nombres, apellidos, nacimiento, contacto, correo, direccion, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
        (ident, first_names, last_names, birth_date, contact, email, address, 1),
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("pacientes"))


@app.route("/eliminar_paciente/<int:id>")
def eliminar_paciente(id):
    cursor = mysql.connection.cursor()
    # update patient for keep information
    delete = datetime.now()
    cursor.execute(
        "UPDATE pacientes SET is_active = %s, eliminacion = %s WHERE id = %s",
        (2, delete, id),
    )
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("pacientes"))


""" citas """


@app.route("/citas")
def citas():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos, pagos.estado, pacientes.is_active
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    JOIN pagos
    ON pagos.cita = citas.id
    """,
    )
    all_data = cursor.fetchall()
    cursor.close()
    return render_template("appointments.html", appointments=all_data)


@app.route("/citas/<int:id>")
def detalle_cita(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos, pacientes.contacto, pacientes.correo, pacientes.is_active
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    WHERE citas.id = %s
    """,
        (id,),
    )
    appointment = cursor.fetchall()
    cursor.execute(
        """
    SELECT pagos.id
    FROM pagos
    WHERE pagos.cita = %s
    """,
        (appointment[0][0],),
    )
    bill_id = cursor.fetchone()[0]
    cursor.close()
    return render_template(
        "appointment-detail.html", appointment=appointment[0], bill_id=bill_id
    )


@app.route("/editar_cita/<int:id>")
def editar_cita(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT citas.*, pacientes.nombres, pacientes.apellidos, pacientes.contacto, pacientes.correo, pagos.estado
    FROM citas
    JOIN pacientes
    ON citas.paciente = pacientes.id
    JOIN pagos
    ON pagos.cita = citas.id
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

    date = request.form["date"]
    start = request.form["start"]
    end = request.form["end"]
    reason = request.form["reason"]
    patient = request.form["patient"]
    cursor = mysql.connection.cursor()

    ## i pass this information for create the appointment after have ready the bill
    ## then i receive this information in '/crear_factura' endpoint

    session["appointmentData"] = {
        "date": date,
        "start": start,
        "end": end,
        "reason": reason,
        "patient": patient,
    }

    cursor.execute(
        """
    SELECT * FROM pacientes
    WHERE id = %s
    """,
        (patient),
    )
    patient_info = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template(
        "create-bill.html",
        patient=patient_info[0],
        date=date,
        start=start,
        end=end,
        reason=reason,
    )


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
    cursor.execute("SELECT * FROM pagos")
    bills = cursor.fetchall()
    cursor.execute(
        """
    SELECT citas.id, citas.estado, pagos.estado
    FROM citas
    JOIN pagos
    ON pagos.cita = citas.id
    """
    )
    appointments = cursor.fetchall()
    cursor.close()
    return render_template(
        "patient-appointment-list.html",
        data=all_data,
        bills=bills,
        appointments=appointments,
    )


""" Facturas """


@app.route("/facturas")
def facturas():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT DISTINCT pacientes.nombres, pacientes.apellidos, pagos.id, pagos.fecha_pago, pagos.valor, pagos.estado, pacientes.is_active
    FROM pagos_pacientes
    JOIN pacientes
    ON pagos_pacientes.id_paciente = pacientes.id
    JOIN citas
    ON pacientes.id = citas.paciente
    JOIN pagos
    ON pagos.id = pagos_pacientes.id_pago
    """
    )
    data = cursor.fetchall()
    cursor.execute(
        """
    SELECT citas.estado, pagos_pacientes.id_pago
    FROM citas
    JOIN pagos
    ON pagos.cita = citas.id
    JOIN pagos_pacientes
    ON pagos_pacientes.id_pago = pagos.id
    JOIN pacientes
    ON pacientes.id = pagos_pacientes.id_paciente
    """
    )
    appointment = cursor.fetchall()
    cursor.close()
    return render_template("bills.html", bills=data, appointments=appointment)


@app.route("/facturas/<int:id>")
def detalle_facturas(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
    SELECT pacientes.nombres, pacientes.apellidos, pacientes.identificacion, pacientes.contacto, pacientes.direccion,
    pagos.valor, pagos.valor_en_letras, pagos.fecha_pago, pagos.descripcion, pagos.id, pagos.estado, pagos.observaciones,
    citas.fecha, citas.ingreso, citas.salida, citas.estado, pagos.metodo_pago
    FROM pagos
    JOIN pagos_pacientes
    ON pagos_pacientes.id_pago = pagos.id
    JOIN pacientes
    ON pacientes.id = pagos_pacientes.id_paciente
    JOIN citas
    ON citas.id = pagos.cita
    WHERE pagos.id = %s
    """,
        (id,),
    )
    data = cursor.fetchall()
    cursor.close()
    date = data[0][7].strftime("%Y-%m-%d")
    appointment_date = data[0][12].strftime("%Y-%m-%d")
    ## para poder mostrar la hora, mirar luego
    """ start = data[0][10].strftime("%H:%M:%S")
    end = data[0][11].strftime("%H:%M:%S") """
    start = str(data[0][13])
    end = str(data[0][14])
    amount = "{:,.2f}".format(data[0][5])
    amount_iva = float(data[0][5] * 0.19)
    iva = "{:,.2f}".format(amount_iva)
    total = "{:,.2f}".format(float(data[0][5]) + float(data[0][5] * 0.19))
    method_paid = data[0][16]
    return render_template(
        "bill-detail.html",
        all_data=data[0],
        date=date,
        appointment_date=appointment_date,
        start=start,
        end=end,
        amount=amount,
        iva=iva,
        total=total,
        method_paid=method_paid,
    )


@app.route("/pagar_factura/<int:id>")
def pagar_factura(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE pagos SET estado = %s WHERE id = %s", (1, id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("detalle_facturas", id=id))


@app.route("/crear_factura")
def crear_factura():
    return render_template("create-bill.html")


@app.route("/guardar_factura", methods=["POST"])
def guardar_factura():
    data = dict(request.form.items())
    if data["appointment-cost"]:
        float(data["appointment-cost"])
    else:
        data["appointment-cost"] = 0.0
    ## buscar paciente por id
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id FROM pacientes WHERE identificacion = %s", ((data["client-id"],))
    )
    # fetchone para traer un solo registro y optimizar el código
    patient_id = cursor.fetchone()[0]

    appointmentData = session.get("appointmentData")

    # Guardamos la información de la cita al momento de generar la factura
    cursor.execute(
        """
    INSERT INTO citas
    (fecha, ingreso, salida, razon, paciente, estado)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
        (
            appointmentData["date"],
            appointmentData["start"],
            appointmentData["end"],
            appointmentData["reason"],
            appointmentData["patient"],
            1,
        ),
    )

    appointment_id = cursor.lastrowid

    if data["pay-check"] == "on":
        pay_status = 1
    else:
        pay_status = 2

    ## guardar la info de los forms en la base de datos del pago
    cursor.execute(
        """
    INSERT INTO pagos (valor, valor_en_letras, descripcion, estado, observaciones, cita, metodo_pago)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
        (
            data["appointment-cost"],
            data["lyric-amount"],
            data["appointment-description"],
            pay_status,
            data["observations"],
            appointment_id,
            data["paid-method"],
        ),
    )

    # guardamos en una variable el valor del último id (de un INSERT o UPDATE) para usarlo en pagos_pacientes
    paid_id = cursor.lastrowid

    ## insertamos el pago relacionado con el paciente en la tabla pagos_pacientes
    cursor.execute(
        "INSERT INTO pagos_pacientes (id_pago, id_paciente) VALUES (%s, %s)",
        (paid_id, patient_id),
    )

    mysql.connection.commit()
    cursor.close()
    return jsonify({"redirect_url": "facturas"})


""" TODA LA LISTA """


@app.route("/historial")
def historial():
    return render_template("all_list.html")


@app.route("/historial/<string:element>")
def historial_detalles(element):
    cursor = mysql.connection.cursor()

    if element == "pacientes":
        cursor.execute("SELECT * FROM pacientes")
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template("all_list.html", patients=data, element=element)

    elif element == "citas":
        cursor.execute(
            """
        SELECT citas.*, pacientes.nombres, pacientes.apellidos, pagos.estado, pacientes.is_active, pagos.fecha_pago
        FROM pacientes
        JOIN citas
        ON citas.paciente = pacientes.id
        JOIN pagos
        ON pagos.cita = citas.id
        """
        )
        data = cursor.fetchall()
        return render_template("all_list.html", appointments=data, element=element)

    elif element == "pagos":
        cursor.execute(
            """
        SELECT DISTINCT pacientes.nombres, pacientes.apellidos, pagos.id, pagos.fecha_pago, pagos.valor, pagos.estado, pacientes.is_active
        FROM pagos_pacientes
        JOIN pacientes
        ON pagos_pacientes.id_paciente = pacientes.id
        JOIN citas
        ON pacientes.id = citas.paciente
        JOIN pagos
        ON pagos.id = pagos_pacientes.id_pago 
        """
        )
        data = cursor.fetchall()
        cursor.execute(
            """
        SELECT citas.estado, pagos_pacientes.id_pago
        FROM citas
        JOIN pagos
        ON pagos.cita = citas.id
        JOIN pagos_pacientes
        ON pagos_pacientes.id_pago = pagos.id
        JOIN pacientes
        ON pacientes.id = pagos_pacientes.id_paciente
        """
        )
        appointment = cursor.fetchall()
        cursor.close()
        return render_template(
            "all_list.html", bills=data, bills_appointments=appointment, element=element
        )


if __name__ == "__main__":
    app.run(debug=True, port=4000)
