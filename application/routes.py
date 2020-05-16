from flask import render_template, request
# app needs to be imported as it's used by decorators below
from application import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
      client_name = request.form['client-name']
      client_phone_number = request.form['client-phone-number']
      """ TODO: rest of form data """
      print(client_name)
      print(client_phone_number)
      if client_name == '' or client_phone_number == '':
        return render_template('index.html', message='Please enter required fields')
    return render_template("success.html")

