from model import db
import datetime
import random

def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs:
        setattr(instance, attr, new_value)
    commit_changes()


def commit_changes():
    db.session.commit()

def convert_json(db_session,my_model, content):
    myTableName = content.get("table")
    credentials = content.get("credentials")
    operation = content.get("operation")
    myTable = getattr(my_model, myTableName)
    myFields = [i for i in myTable.__dict__.keys() if i[:1] != '_']
    fieldValues = [content.get(field) for field in myFields]
    if operation == "update":
        if "last_update_datetime" in myFields:
            fieldValues[myFields.index("last_update_datetime")] = datetime.datetime.utcnow()
    elif operation == "insert":
        fieldValues[myFields.index("id")] = random.randint(10 ** 15, (10 ** 16) - 1)  # inserts the id
        if "create_datetime" in myFields:
            fieldValues[myFields.index("create_datetime")] = datetime.datetime.utcnow()
    for index, field in enumerate(fieldValues):
        if field == "None":
            fieldValues[index] = db_session.null()
    myDict = {}
    for i, fieldName in enumerate(myFields):
        myDict[fieldName] = fieldValues[i]
    return myDict,myTable