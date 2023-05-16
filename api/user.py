from flask import request, jsonify
from flask_restful import abort, Resource
from app import db
from marshmallow import Schema, fields
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
import random
import string

#User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    as_employee = db.Column(db.Boolean, default=False)
    as_company = db.Column(db.Boolean, default=False)
    subscribe_email = db.Column(db.Boolean, default=False)
    subscribe_sms = db.Column(db.Boolean, default=False)

    jobs = db.relationship(
        'Job',
        backref='user',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Job.timestamp)'
    )

    candidates = db.relationship(
        'Candidate',
        backref='user',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Candidate.timestamp)'
    )

    feedback = db.relationship(
        'Feedback',
        backref='user',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Feedback.timestamp)'
    )

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, firstname, lastname, email, phone, password,
    as_employee, as_company, subscribe_email, subscribe_sms, timestamp):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.password = password
        self.as_employee = as_employee
        self.as_company = as_company
        self.subscribe_email = subscribe_email
        self.subscribe_sms = subscribe_sms
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

db.create_all()
db.session.commit()

from api.job import JobSchema
from api.candidate import CandidateSchema
from api.feedback import FeedbackSchema

# User Schema
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str()
    lastname = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    password = fields.Str()
    as_employee = fields.Boolean()
    as_company = fields.Boolean()
    subscribe_email = fields.Boolean()
    subscribe_sms = fields.Boolean()
    jobs = fields.Nested(JobSchema, many=True)
    candidates = fields.Nested(CandidateSchema, many=True)
    feedback = fields.Nested(FeedbackSchema, many=True)

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#User Login Class
class UserLogin(Resource):
    def post(self):
        req = request.json
        email = req['email']
        password = req['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error' : 'User email not exist'})
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            if not user.feedback:
                feedback = False
            else:
                feedback = True

            return jsonify({
                'token' : access_token,
                'user_id' : user.id, 
                'user_firstname' : user.firstname,
                'user_as_company' : user.as_company,
                'user_as_employee' : user.as_employee,
                'user_feedback' : feedback
            })
        else:
            return jsonify({'error' : 'Incorrect password'})

#User Signup Class
class UserSignup(Resource):
    def post(self):
        fname = request.json['firstname']
        lname = request.json['lastname']
        email = request.json['email']
        phone = request.json['phone']
        password = request.json['password']
        asEmployee = request.json['as_employee']
        asCompany = request.json['as_company']
        subscribeEmail = request.json['subscribe_email']
        subscribeSms = request.json['subscribe_sms']
        hash_password = generate_password_hash(password, method='sha256')

        new_user = User(
            firstname=fname, 
            lastname=lname, 
            email=email, 
            phone=phone, 
            password=hash_password, 
            as_employee=asEmployee, 
            as_company=asCompany, 
            subscribe_email=subscribeEmail,
            subscribe_sms=subscribeSms,
            timestamp=date_time
        )

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'error' : 'Email already Taken!'})

        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201

#User Reset Password Class
class UserReset(Resource):
    def post(self):
        email = request.json['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error' : 'User email not exist'})

        # generate password
        length = 10
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        all = lower + upper + num
        temp = random.sample(all,length)
        password = "".join(temp)
        print(password)

        # store the password
        hash_password = generate_password_hash(password, method='sha256')
        print(hash_password)
        user.password = hash_password
        db.session.commit()
        return jsonify({'message' : 'reset password successfully'})

        # send email


#User List Class
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

#User by ID Class
class UserID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User doesn't exist")
        return user_schema.dump(user)

    @jwt_required()
    def put(self, id):
        data = request.json
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User doesn't exist, cannot update")

        if not data['password'] == '':
            hash_password = generate_password_hash(data['password'], method='sha256')
            user.password = hash_password

        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.email = data['email']
        user.phone = data['phone']
        user.as_employee = data['as_employee']
        user.as_company = data['as_company']
        user.subscribe_email = data['subscribe_email']
        user.subscribe_sms = data['subscribe_sms']
        db.session.commit()
        return user_schema.dump(user)

    @jwt_required()
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User doesn't exist")

        db.session.delete(user)
        db.session.commit()
        return '', 204 