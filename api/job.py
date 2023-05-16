from flask import request, jsonify
from flask_restful import abort, Resource
from app import db
from marshmallow import Schema, fields
from datetime import datetime
from api.user import User
from flask_jwt_extended import jwt_required
from sqlalchemy import or_, and_, select, func, Integer, Table, Column, MetaData, distinct

#Job Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    company_name = db.Column(db.String(100), nullable=False)
    company_address = db.Column(db.String(100), nullable=False)
    company_city = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    job_status = db.Column(db.String(15), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    search_count = db.Column(db.Integer, default=0)

    required_skills = db.relationship(
        'RequiredSkill',
        backref='job',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(RequiredSkill.timestamp)'
    )

    requirements = db.relationship(
        'Requirement',
        backref='job',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Requirement.timestamp)'
    )

    preferreds = db.relationship(
        'Preferred',
        backref='job',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Preferred.timestamp)'
    )

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    

    def __init__(self, user_id, company_name, company_address, company_city, contact_name, 
    contact_email, contact_phone, job_title, job_location, job_status, job_description, search_count, timestamp):
        self.user_id = user_id
        self.company_name = company_name
        self.company_address = company_address
        self.company_city = company_city
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.job_title = job_title
        self.job_location = job_location
        self.job_status = job_status
        self.job_description = job_description
        self.search_count = search_count
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

#RequiredSkill Model
class RequiredSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    required_skill = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, job_id, required_skill, timestamp):
        self.job_id = job_id
        self.required_skill = required_skill
        self.timestamp = timestamp
        

    def __repr__(self):
        return self.id

#Requirement Model
class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    required = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, job_id, required, timestamp):
        self.job_id = job_id
        self.required = required
        self.timestamp = timestamp
        

    def __repr__(self):
        return self.id

#Preferred Model
class Preferred(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    preferred = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, job_id, preferred, timestamp):
        self.job_id = job_id
        self.preferred = preferred
        self.timestamp = timestamp
        

    def __repr__(self):
        return self.id

db.create_all()
db.session.commit()

# RequiredSkill Schema
class RequiredSkillSchema(Schema):
    required_skill = fields.Str()

# Requirement Schema
class RequirementSchema(Schema):
    required = fields.Str()

# Preferred Schema
class PreferredSchema(Schema):
    preferred = fields.Str()

# Job Schema
class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    company_name = fields.Str()
    company_address = fields.Str()
    company_city = fields.Str()
    contact_name = fields.Str()
    contact_email = fields.Str()
    contact_phone = fields.Str()
    job_title = fields.Str()
    job_location = fields.Str()
    job_status =  fields.Str()
    job_description = fields.Str()
    search_count = fields.Int()
    timestamp = fields.Date()
    required_skills = fields.Nested(RequiredSkillSchema, many=True)
    requirements = fields.Nested(RequirementSchema, many=True)
    preferreds = fields.Nested(PreferredSchema, many=True)

class JobFrequentlySchema(Schema):
    count_1 = fields.Int()
# Init schema
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
job_frequently = JobFrequentlySchema()
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Job Search Class
class JobSearch(Resource):
    def get(self):
        per_page = 9
        page = request.args.get('page', type = int)
        keyword = request.args.get("keyword").lower() if request.args.get("keyword") != None else ''
        location = request.args.get("location").lower() if request.args.get("location") != None else ''

        if keyword != '':
            jobs = Job.query.filter(or_(
                Job.company_name.ilike('%' + keyword + '%'), 
                Job.job_title.ilike('%' + keyword + '%'))
                ).paginate(page,per_page,error_out=False)
            if jobs.total < 1:
                jobs = Job.query.join(Job.required_skills).filter(RequiredSkill.required_skill.ilike('%' + keyword + '%')).paginate(page,per_page,error_out=False)
                
        elif location != '':
            jobs = Job.query.filter(or_(
                Job.job_location.ilike('%' + location + '%'), 
                Job.company_address.ilike('%' + location + '%'))
                ).paginate(page,per_page,error_out=False)


        total_page = jobs.pages
        page_num = page
        returnData = {}
        returnData['total_page'] = total_page
        returnData['page_num'] = page_num
        resultData = jobs_schema.dump(jobs.items)
        return jsonify(resultData, returnData)

#Job Search Class
class JobSearchCount(Resource):
    def get(self):
        jobs = Job.query.order_by(Job.search_count.desc())
        return jobs_schema.dump(jobs)

#Job Frequently Class
class JobFrequently(Resource):
    def get(self):
        jobQueries = Job.query.with_entities(Job.job_title, func.count(Job.job_title)).group_by(Job.job_title).order_by(func.count(Job.job_title).desc())
        data = []
        for row in jobQueries:
            dataQuery = {}
            dataQuery['job_title'] = row[0]
            dataQuery['count'] = row[1]
            data.append(dataQuery)

        return jsonify(data)

#Job List Class
class JobList(Resource):
    def get(self, page):
        per_page = 9
        jobs = Job.query.order_by(Job.timestamp.desc()).paginate(page,per_page,error_out=False)
        total_page = jobs.pages
        page_num = page
        returnData = {}
        returnData['total_page'] = total_page
        returnData['page_num'] = page_num
        resultData = jobs_schema.dump(jobs.items)
        return jsonify(resultData, returnData)

#Job Post Class
class JobPost(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        userID = data['user_id']
        user = User.query.filter_by(id=userID).first()
        if not user:
            abort(404, message="User doesn't exist, cannot create Job data")

        if not user.as_company == True:
            abort(404, message="User not as Job role, cannot create Job data")

        companyName = data['company_name']
        companyAddress = data['company_address']
        companyCity = data['company_city']
        contactName = data['contact_name']
        contactEmail = data['contact_email']
        contactPhone = data['contact_phone']
        jobTitle = data['job_title']
        jobLocation = data['job_location']
        jobStatus = data['job_status']
        jobDescription = data['job_description']
        searchCount = data['search_count']

        job = Job(
            user_id=userID, 
            company_name=companyName, 
            company_address=companyAddress, 
            company_city=companyCity, 
            contact_name=contactName, 
            contact_email=contactEmail, 
            contact_phone=contactPhone, 
            job_title=jobTitle, 
            job_location=jobLocation, 
            job_status=jobStatus,
            job_description=jobDescription, 
            search_count=searchCount,
            timestamp=date_time
        )

        db.session.add(job)
        db.session.flush()
        job_id = job.id

        for reqSkill in data['required_skills']:
            reqSkill = reqSkill['required_skill']
            required_skill = RequiredSkill(
                job_id=job_id,
                required_skill=reqSkill,
                timestamp=date_time
            )
            db.session.add(required_skill)

        for requirement in data['requirements']:
            require = requirement['required']
            required = Requirement(
                job_id=job_id,
                required=require,
                timestamp=date_time
            )
            db.session.add(required)

        for preferred in data['preferreds']:
            prefer = preferred['preferred']
            preferr = Preferred(
                job_id=job_id,
                preferred=prefer,
                timestamp=date_time
            )
            db.session.add(preferr)

        db.session.commit()

        return job_schema.dump(job), 201


#Job ID Class
class JobID(Resource):
    def get(self, id):
        job = Job.query.filter_by(id=id).first()
        if not job:
            abort(404, message="Job doesn't exist")
        return job_schema.dump(job)

    @jwt_required()
    def put(self, id):
        job = Job.query.filter_by(id=id).first()
        if not job:
            abort(404, message="Job doesn't exist, cannot update")

        data = request.json
        job.user_id = data['user_id']
        user = User.query.filter_by(id=job.user_id).first()
        if not user:
            abort(404, message="User doesn't exist, cannot update Job data")

        if not user.as_company == True:
            abort(404, message="User not as Job role, cannot update Job data")

        job.company_name = data['company_name']
        job.company_address = data['company_address']
        job.company_city = data['company_city']
        job.contact_name = data['contact_name']
        job.contact_email = data['contact_email']
        job.contact_phone = data['contact_phone']
        job.job_title = data['job_title']
        job.job_location = data['job_location']
        job.job_status = data['job_status']
        job.job_description = data['job_description']
        job.search_count = data['search_count']
        db.session.add(job)

        RequiredSkill.query.filter_by(job_id=id).delete()
        for reqSkill in data['required_skills']:
            reqSkill = reqSkill['required_skill']
            required_skill = RequiredSkill(
                job_id=id,
                required_skill=reqSkill,
                timestamp=date_time
            )
            db.session.add(required_skill)

        Requirement.query.filter_by(job_id=id).delete()
        for requirement in data['requirements']:
            require = requirement['required']
            required = Requirement(
                job_id=id,
                required=require,
                timestamp=date_time
            )
            db.session.add(required)

        Preferred.query.filter_by(job_id=id).delete()
        for preferred in data['preferreds']:
            prefer = preferred['preferred']
            preferr = Preferred(
                job_id=id,
                preferred=prefer,
                timestamp=date_time
            )
            db.session.add(preferr)

        db.session.commit()
        return job_schema.dump(job)

    @jwt_required()
    def delete(self, id):
        job = Job.query.filter_by(id=id).first()
        if not job:
            abort(404, message="Job doesn't exist")

        db.session.delete(job)
        db.session.commit()
        return '', 204

#Job ViewCount Class
class JobViewCount(Resource):
    def put(self, id):
        job = Job.query.filter_by(id=id).first()
        if not job:
            abort(404, message="Job doesn't exist")

        job.search_count = request.json['search_count']

        db.session.add(job)
        db.session.commit()
        return jsonify({'message': 'Success'})
