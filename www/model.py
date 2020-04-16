import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Tenant(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(256), index=True, unique=True)
    status = db.Column(db.String(64))
    create_datetime = db.Column(db.DateTime)
    def __repr__(self):
        return '<Tenant {}>'.format(self.name)

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Patient(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    mobile_number = db.Column(db.String(25))
    postal_address = db.Column(db.Integer)
    create_datetime = db.Column(db.DateTime)
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)
    def __repr__(self):
        return 'Patient: %r' % self.name

class PatientLogin(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'), nullable=False)
    password_hash = db.Column(db.String(128))
    last_login_datetime = db.Column(db.DateTime)
    def __repr__(self):
            return 'Patient id: %r | Time: %r' % (self.patient_id,self.last_login_datetime)


class ResultCategory(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    score_range = db.Column(db.String(128), nullable=False)
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)

class PatientRequest(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('result_category.id'), nullable=False)
    status = db.Column(db.String(128), unique=False, nullable=False)
    create_datetime = db.Column(db.DateTime)
    last_update_datetime = db.Column(db.DateTime)
    last_updated_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return 'Patient Request Id: %r' % self.id

class NotificationTemplate(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('result_category.id'), nullable=False)
    message_body = db.Column(db.Text)
    create_datetime = db.Column(db.DateTime)
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)

class PatientNotification(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    request_id = db.Column(db.BigInteger, db.ForeignKey('patient_request.id'), nullable=False)
    template_id = db.Column(db.BigInteger, db.ForeignKey('notification_template.id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime)
    status = db.Column(db.String(128), unique=False, nullable=False)
    sent_datetime = db.Column(db.DateTime)

class Symptom(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    symptom_description = db.Column(db.String(2048))
    scale = db.Column(db.Integer)
    correlated_factor = db.Column(db.Float)
    binary = db.Column(db.Boolean)
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)

class AgeGroup(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    range = db.Column(db.String(64))
    correlated_factor = db.Column(db.Float)
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)

class AcuteSymptom(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    symptom_description = db.Column(db.String(2048))
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)

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
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)

class GuideContent(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(2048))
    url = db.Column(db.String(256), index=True, unique=True)
    tenant_id = db.Column(db.BigInteger, db.ForeignKey('tenant.id'), nullable=False)
