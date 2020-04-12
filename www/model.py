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
    url = db.Column(db.String(256), index=True, unique=True)
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
    mobile_number = db.Column(db.String(25))
    postal_address = db.Column(db.Integer)
    create_datetime = db.Column(db.DateTime)
    tenant_id = db.relationship('Tenant', backref="patient", lazy="dynamic")
    def __repr__(self):
        return 'Patient: %r' % self.name

class PatientRequest(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.relationship('Patient', backref="request", lazy="dynamic")
    category_id = db.relationship('ResultCategory', backref="request", lazy="dynamic")
    status = db.Column(db.String(128), unique=False, nullable=False)
    create_datetime = db.Column(db.DateTime)
    last_update_datetime = db.Column(db.DateTime)
    last_updated_user_id = db.relationship('User', backref="request", lazy="dynamic")
    def __repr__(self):
        return 'Patient Request Id: %r' % self.id

class ResultCategory(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    score_range = db.Column(db.String(128), nullable=False)
    tenant_id = db.relationship('Tenant', backref="result_category", lazy="dynamic")

class PatientNotification(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    request_id = db.relationship('Request', backref="notification", lazy="dynamic")
    template_id = db.relationship('NotificationTemplate', backref="notification", lazy="dynamic")
    tenant_id = db.relationship('Tenant', backref="notification", lazy="dynamic")
    message_body = db.Column(db.Text)
    create_datetime = db.Column(db.DateTime)

class Symptom(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    symptom_description = db.Column(db.String(2048))
    scale = db.Column(db.Integer)
    correlated_factor = db.Column(db.Float)
    binary = db.Column(db.Boolean)
    tenant_id = db.relationship('Tenant', backref="symptom", lazy="dynamic")

class AgeGroup(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    range = db.Column(db.String(64))
    correlated_factor = db.Column(db.Float)
    tenant_id = db.relationship('Tenant', backref="age_group", lazy="dynamic")

class AcuteSymptom(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    symptom_description = db.Column(db.String(2048))
    tenant_id = db.relationship('Tenant', backref="acute_symptom", lazy="dynamic")

class Gender(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(128))
    correlated_factor = db.Column(db.Float)

class UnderlyingDisease(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(2048))
    scale = db.Column(db.Integer)
    correlated_factor = db.Column(db.Float)
    binary = db.Column(db.Boolean)
    tenant_id = db.relationship('Tenant', backref="underlying_disease", lazy="dynamic")

class GuideContent(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(2048))
    url = db.Column(db.String(256), index=True, unique=True)
    tenant_id = db.relationship('Tenant', backref="guidecontent", lazy="dynamic")
