# Infrastructure test page.
import os
from flask import Flask
from flask import Markup
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from init import create_app
from model import db
import dbhelper


app = create_app()

@app.route("/")
def test():
    mysql_result = False
    query_string = text("select concat(table_schema,'.',table_name) from information_schema.tables where table_schema = 'patient_sass'")
    rows = db.engine.execute(query_string)

    # Return the page with the result.
    return render_template('db-test.html', rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
