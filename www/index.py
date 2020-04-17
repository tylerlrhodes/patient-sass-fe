# Infrastructure test page.
import os
import random
from flask import Flask
from flask import Markup
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from init import create_app,load_init_data
from model import db,User,Patient,Symptom
import dbhelper


app = create_app()

db = SQLAlchemy(app)
db.create_all()
load_init_data()


@app.route("/test_vue")
def test_vue():
    return render_template('vue.html', name="vue-test")

@app.route("/test_db")
def test_db():
    n = random.randint(0, 10000)
    str = f'abc{n}'
    p = Patient(name=str)
    db.session.add(p)
    db.session.commit()
    for p in Patient.query.all():
        str += p.__repr__() + "<br />"
    result = Markup(f'<span style="color: green;">Init DB<br />{str}</span>')
    return render_template('test-patient.html', result=result)

@app.route("/")
@app.route("/symptoms")
def handle_symptoms():
  symptoms_json_arr = [s.to_json() for s in Symptom.query.all()]
  symptoms_json = "[" + ",".join(symptoms_json_arr) + "]"
  return render_template('vue.html', name="symptoms", symptoms_json=symptoms_json)

@app.route("/test-tables")
def test():
    mysql_result = False
    query_string = text("select concat(table_schema,'.',table_name) from information_schema.tables where table_schema = 'patient_sass'")
    rows = db.engine.execute(query_string)

    # Return the page with the result.
    return render_template('db-test.html', rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
