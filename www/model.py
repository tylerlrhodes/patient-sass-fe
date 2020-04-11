import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    tenant_id = db.relationship('Tenant', backref="user", lazy="dynamic")
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Tenant(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(128), index=True, unique=True)
    status = db.Column(db.String(64))
    create_datetime = db.Column(db.DateTime)
    def __repr__(self):
        return '<Tenant {}>'.format(self.name)


class PatientLogin(db.Model):
    patient_id = db.relationship('Patient',backref="login", lazy="dynamic")
    id = db.Column(db.BigInteger, primary_key=True)
    password_hash = db.Column(db.String(128))
    last_login_datetime = db.Column(db.DateTime)
    def __repr__(self):
            return 'Patient id: %r | Time: %r' % (self.patient_id,self.last_login_datetime)
class Patient(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    mobile_number = db.Column(db.string(25))
    postal_address = db.Column(db.Integer)
    create_datetime = db.Column(db.DateTime)
    tenant_id = db.relationship('Tenant', backref="patient", lazy="dynamic")
    def __repr__(self):
        return 'Patient: %r' % self.name

class PatientRequest(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.relationship('Patient', backref="request", lazy="dynamic")
    category_id = db.Column(db.BigInteger)
    status = db.Column(db.String(128), unique=False, nullable=False)
    create_datetime = db.Column(db.DateTime)
    last_update_datetime = db.Column(db.DateTime)
    last_updated_user_id = db.relationship('User', backref="request", lazy="dynamic")