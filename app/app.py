from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("pacientes"))

@app.route("/pacientes")
def pacientes():
    return render_template("patients.html")

if __name__ == "__main__":
    app.run(debug=True, port=4000)