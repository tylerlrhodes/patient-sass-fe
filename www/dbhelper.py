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


def edit_instance(model, idin, **kwargs):
    instance = model.query.filter_by(id=idin).all()[0]
    for attr, new_value in kwargs:
        setattr(instance, attr, new_value)
    commit_changes()


def commit_changes():
    db.session.commit()

#Takes a db_session, a str representing which table to use and the request as a Dict and creates serveral useful variables
#Like the final dictionary for db operation
def convert_json(db_session,my_model, content):
    myTableName = content.get("table")
    credentials = content.get("credentials")
    operation = content.get("operation")
    myTable = getattr(my_model, myTableName)
    myFields = [i for i in myTable.__dict__.keys() if i[:1] != '_']
    fieldValues = [content.get(field) for field in myFields]
    id = None
    if operation == "update": #If it is an updated we dont neeed all fields
        myFields = [i for i in content.keys() if i not in ["table","credentials","operation"]] #gets only the ones we have on the request
        fieldValues = [content.get(field) for field in myFields ]
        if "last_update_datetime" in myFields: #creates datetime
            fieldValues[myFields.index("last_update_datetime")] = datetime.datetime.utcnow()
            id = fieldValues[myFields.index("id")]
    elif operation == "insert":
        id = random.randint(10 ** 15, (10 ** 16) - 1)
        fieldValues[myFields.index("id")] = id  # inserts the id
        if "create_datetime" in myFields:
            fieldValues[myFields.index("create_datetime")] = datetime.datetime.utcnow() #inserts created datetime
    for index, field in enumerate(fieldValues):
        if field == "None": #places the correct null values
            fieldValues[index] = db_session.null()
    myDict = {}
    for i, fieldName in enumerate(myFields): #creates the final dictionary of values
        myDict[fieldName] = fieldValues[i]
    return myDict,myTable,operation,id