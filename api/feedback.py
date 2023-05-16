from flask import request
from flask_restful import abort, Resource
from app import db
from marshmallow import Schema, fields
from datetime import datetime
from api.user import User
from flask_jwt_extended import jwt_required

#Feedback Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    feedback_point = db.Column(db.Integer, nullable=False)
    feedback_comment = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, user_id, feedback_point, feedback_comment, timestamp):
        self.user_id = user_id
        self.feedback_point = feedback_point
        self.feedback_comment = feedback_comment
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

db.create_all()
db.session.commit()

#Feedback Schema
class FeedbackSchema(Schema):
        user_id = fields.Int()
        feedback_point = fields.Int()
        feedback_comment = fields.Str()

#Init schema
feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Feedback List Class
class FeedbackList(Resource):
    def get(self):
        feedbacks = Feedback.query.order_by(Feedback.timestamp.desc())
        return feedbacks_schema.dump(feedbacks)

    @jwt_required()
    def post(self):
        userID = request.json['user_id']
        user = User.query.filter_by(id=userID).first()
        if not user:
            abort(404, message="User doesn't exist, cannot send feedback")
        
        feedbackPoint = request.json['feedback_point']
        feedbackComment = request.json['feedback_comment']

        new_feedback = Feedback(
            user_id=userID, 
            feedback_point=feedbackPoint, 
            feedback_comment=feedbackComment,
            timestamp=date_time
        )

        feedback = Feedback.query.filter_by(user_id=userID).first()
        if feedback:
            abort(409, message='This user already gave feedback')

        db.session.add(new_feedback)
        db.session.commit()
        return feedback_schema.dump(new_feedback), 201


#Feedback by ID Class
class FeedbackID(Resource):
    def get(self, id):
        feedback = Feedback.query.filter_by(id=id).first()
        if not feedback:
            abort(404, message="Feedback doesn't exist")
        return feedback_schema.dump(feedback)