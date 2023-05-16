from flask import jsonify, request
from flask_restful import abort, Resource
from app import db
from marshmallow import Schema, fields
from datetime import datetime
from api.user import User
from flask_jwt_extended import jwt_required
from sqlalchemy import or_, and_

#Candidate Model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    post_code = db.Column(db.String(15), nullable=False)
    about_me = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    cv = db.Column(db.String(255), nullable=False)

    educations = db.relationship(
        'Education',
        backref='candidate',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Education.timestamp)'
    )

    experiences = db.relationship(
        'Experience',
        backref='candidate',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Experience.timestamp)'
    )

    skills = db.relationship(
        'Skill',
        backref='candidate',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Skill.timestamp)'
    )

    languages = db.relationship(
        'Language',
        backref='candidate',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Language.timestamp)'
    )

    social_media = db.relationship(
        'SocialMedia',
        backref='candidate',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(SocialMedia.timestamp)'
    )

    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    

    def __init__(self, user_id, firstname, lastname, email, phone, title, date_of_birth, 
    address, city, post_code, about_me, picture, cv,timestamp):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.title = title
        self.date_of_birth = date_of_birth
        self.address = address
        self.city = city
        self.post_code = post_code
        self.about_me = about_me
        self.picture = picture
        self.cv = cv
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

#Education Model
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    education_name = db.Column(db.String(255), nullable=False)
    graduation_date = db.Column(db.DateTime)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, candidate_id, education_name, graduation_date, timestamp):
        self.candidate_id = candidate_id
        self.education_name = education_name
        self.graduation_date = graduation_date
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

#Experience Model
class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    company = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    position_job = db.Column(db.String(100), nullable=False)
    description_job = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, candidate_id, company, start_date, end_date, position_job, description_job, timestamp):
        self.candidate_id = candidate_id
        self.company = company
        self.start_date = start_date
        self.end_date = end_date
        self.position_job = position_job
        self.description_job = description_job
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

#Skill Model
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    skill_name = db.Column(db.String(100), nullable=False)
    skill_level = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, candidate_id, skill_name, skill_level, timestamp):
        self.candidate_id = candidate_id
        self.skill_name = skill_name
        self.skill_level = skill_level
        self.timestamp = timestamp
        

    def __repr__(self):
        return self.id

#Language Model
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    language_name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, candidate_id, language_name, level, timestamp):
        self.candidate_id = candidate_id
        self.language_name = language_name
        self.level = level
        self.timestamp = timestamp

    def __repr__(self):
        return self.id

#Social Media Model
class SocialMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"))
    social_media_name = db.Column(db.String(100), nullable=False)
    social_media_url = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, candidate_id, social_media_name, social_media_url, timestamp):
        self.candidate_id = candidate_id
        self.social_media_name = social_media_name
        self.social_media_url = social_media_url
        self.timestamp = timestamp
        

    def __repr__(self):
        return self.id

db.create_all()
db.session.commit()

# Education Schema
class EducationSchema(Schema):
    education_name = fields.Str()
    graduation_date = fields.Date()

# Experience Schema
class ExperienceSchema(Schema):
    company = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    position_job = fields.Str()
    description_job = fields.Str()

# Skill Schema
class SkillSchema(Schema):
    skill_name = fields.Str()
    skill_level = fields.Str()

# Language Schema
class LanguageSchema(Schema):
    language_name = fields.Str()
    level = fields.Str()

# Social Media Schema
class SocialMediaSchema(Schema):
    social_media_name = fields.Str()
    social_media_url = fields.Str()

# Candidate Schema
class CandidateSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    firstname = fields.Str()
    lastname = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    title = fields.Str()
    date_of_birth = fields.Date()
    address = fields.Str()
    city = fields.Str()
    post_code =  fields.Str()
    about_me = fields.Str()
    picture = fields.Str()
    cv = fields.Str()
    educations = fields.Nested(EducationSchema, many=True)
    experiences = fields.Nested(ExperienceSchema, many=True)
    skills = fields.Nested(SkillSchema, many=True)
    languages = fields.Nested(LanguageSchema, many=True)
    social_media = fields.Nested(SocialMediaSchema, many=True)

# Init schema
experience_schema = ExperienceSchema(many=True)
candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Candidate Search Class
class CandidateSearch(Resource):
    def get(self):
        per_page = 9
        page = request.args.get('page', type = int)
        keyword = request.args.get("keyword").lower() if request.args.get("keyword") != None else ''
        location = request.args.get("location").lower() if request.args.get("location") != None else ''
        education = request.args.get("education").lower() if request.args.get("education") != None else ''
        company = request.args.get("company").lower() if request.args.get("company") != None else ''
        language = request.args.get("language").lower() if request.args.get("language") != None else ''
        birthFrom = request.args.get("birth_from").lower() if request.args.get("birth_from") != None else ''
        birthTo = request.args.get("birth_to").lower() if request.args.get("birth_to") != None else ''

        if keyword != '':
            candidates = Candidate.query.filter(Candidate.title.ilike('%' + keyword + '%')).paginate(page,per_page,error_out=False)
            if candidates.total < 1:
                candidates = Candidate.query.join(Candidate.skills).filter(Skill.skill_name.ilike('%' + keyword + '%')).paginate(page,per_page,error_out=False)
        elif location != '':
            candidates = Candidate.query.filter(or_(
                Candidate.address.ilike('%' + location + '%'), 
                Candidate.city.ilike('%' + location + '%'))
                ).paginate(page,per_page,error_out=False)
        elif education != '':
            candidates = Candidate.query.join(Candidate.educations).filter(
                Education.education_name.ilike('%' + education + '%')
                ).paginate(page,per_page,error_out=False)
        elif company != '':
            candidates = Candidate.query.join(Candidate.experiences).filter(
                Experience.company.ilike('%' + company + '%')
                ).paginate(page,per_page,error_out=False)
        elif language != '':
            candidates = Candidate.query.join(Candidate.languages).filter(
                Language.language_name.ilike('%' + language + '%')
                ).paginate(page,per_page,error_out=False)
        elif birthFrom != '' and birthTo != '':
            candidates = Candidate.query.filter(and_(
                Candidate.date_of_birth <= birthTo, 
                Candidate.date_of_birth >= birthFrom
                )).paginate(page,per_page,error_out=False)

        total_page = candidates.pages
        page_num = page
        returnData = {}
        returnData['total_page'] = total_page
        returnData['page_num'] = page_num
        resultData = candidates_schema.dump(candidates.items)
        return jsonify(resultData, returnData)


#Candidate List Class
class CandidateList(Resource):
    def get(self, page):
        per_page = 9
        candidates = Candidate.query.order_by(Candidate.timestamp.desc()).paginate(page,per_page,error_out=False)
        total_page = candidates.pages
        page_num = page
        returnData = {}
        returnData['total_page'] = total_page
        returnData['page_num'] = page_num
        resultData = candidates_schema.dump(candidates.items)
        return jsonify(resultData, returnData)

    @jwt_required()
    def post(self):
        data = request.json
        userID = data['user_id']
        user = User.query.filter_by(id=userID).first()
        if not user:
            abort(404, message="User doesn't exist, cannot create Candidate data")

        if not user.as_employee == True:
            abort(404, message="User not as Candidate role, cannot create Candidate data")

        fname = data['firstname']
        lname = data['lastname']
        email = data['email']
        phone = data['phone']
        title = data['title']
        dateOfBirth = datetime.strptime(data['date_of_birth'], "%d/%m/%Y")
        address = data['address']
        city = data['city']
        postCode = data['post_code']
        about_me = data['about_me']
        picture = data['picture']
        cv = data['cv']

        candidate = Candidate(
            user_id=userID, 
            firstname=fname, 
            lastname=lname, 
            email=email, 
            phone=phone, 
            title=title, 
            date_of_birth=dateOfBirth, 
            address=address, 
            city=city, 
            post_code=postCode,
            about_me=about_me, 
            picture=picture,
            cv=cv,
            timestamp=date_time
        )

        db.session.add(candidate)
        db.session.flush()
        candidate_id = candidate.id

        for eduData in data['educations']:
            edu = eduData['education_name']
            graduate = eduData['graduation_date']
            education = Education(
                candidate_id=candidate_id,
                education_name=edu,
                graduation_date=datetime.strptime(graduate, "%d/%m/%Y"),
                timestamp=date_time
            )
            db.session.add(education)

        for expData in data['experiences']:
            company = expData['company']
            start_date = expData['start_date']
            end_date = expData['end_date']
            position_job = expData['position_job']
            description_job = expData['description_job']
            experience = Experience(
                candidate_id=candidate_id,
                company=company,
                start_date=datetime.strptime(start_date, "%d/%m/%Y"),
                end_date=datetime.strptime(end_date, "%d/%m/%Y"),
                position_job=position_job,
                description_job=description_job,
                timestamp=date_time
            )
            db.session.add(experience)

        for skillData in data['skills']:
            skillName = skillData['skill_name']
            skillLevel = skillData['skill_level']
            skills = Skill(
                candidate_id=candidate_id,
                skill_name=skillName,
                skill_level=skillLevel,
                timestamp=date_time
            )
            db.session.add(skills)
        
        for langData in data['languages']:
            lang = langData['language_name']
            level = langData['level']
            languages = Language(
                candidate_id=candidate_id,
                language_name=lang,
                level=level,
                timestamp=date_time
            )
            db.session.add(languages)

        for sosmedData in data['social_media']:
            sosmedName = sosmedData['social_media_name']
            sosmedLevel = sosmedData['social_media_url']
            sosmeds = SocialMedia(
                candidate_id=candidate_id,
                social_media_name=sosmedName,
                social_media_url=sosmedLevel,
                timestamp=date_time
            )
            db.session.add(sosmeds)

        db.session.commit()
        
        return candidate_schema.dump(candidate), 201
        


#Candidate Class
class CandidateID(Resource):
    def get(self, id):
        candidate = Candidate.query.filter_by(id=id).first()
        if not candidate:
            abort(404, message="Candidate doesn't exist")
        return candidate_schema.dump(candidate)

    @jwt_required()
    def put(self, id):
        candidate = Candidate.query.filter_by(id=id).first()
        if not candidate:
            abort(404, message="Candidate doesn't exist, cannot update")

        data = request.json
        candidate.user_id = data['user_id']
        user = User.query.filter_by(id=candidate.user_id).first()
        if not user:
            abort(404, message="User doesn't exist, cannot update Candidate data")

        if not user.as_employee == True:
            abort(404, message="User not as Candidate role, cannot update Candidate data")

        candidate.firstname = data['firstname']
        candidate.lastname = data['lastname']
        candidate.email = data['email']
        candidate.phone = data['phone']
        candidate.title = data['title']
        candidate.date_of_birth = datetime.strptime(data['date_of_birth'], "%d/%m/%Y")
        candidate.address = data['address']
        candidate.city = data['city']
        candidate.post_code = data['post_code']
        candidate.about_me = data['about_me']
        candidate.picture = data['picture']
        candidate.cv = data['cv']
        candidate.timestamp = date_time
        db.session.add(candidate)

        Education.query.filter_by(candidate_id=id).delete()
        for eduData in data['educations']:
            edu = eduData['education_name']
            graduate = eduData['graduation_date']
            education = Education(
                candidate_id=id,
                education_name=edu,
                graduation_date=datetime.strptime(graduate, "%d/%m/%Y"),
                timestamp=date_time
            )
            db.session.add(education)

        Experience.query.filter_by(candidate_id=id).delete()
        for expData in data['experiences']:
            company = expData['company']
            start_date = expData['start_date']
            end_date = expData['end_date']
            position_job = expData['position_job']
            description_job = expData['description_job']
            experience = Experience(
                candidate_id=id,
                company=company,
                start_date=datetime.strptime(start_date, "%d/%m/%Y"),
                end_date=datetime.strptime(end_date, "%d/%m/%Y"),
                position_job=position_job,
                description_job=description_job,
                timestamp=date_time
            )
            db.session.add(experience)

        Skill.query.filter_by(candidate_id=id).delete()
        for skillData in data['skills']:
            skillName = skillData['skill_name']
            skillLevel = skillData['skill_level']
            skills = Skill(
                candidate_id=id,
                skill_name=skillName,
                skill_level=skillLevel,
                timestamp=date_time
            )
            db.session.add(skills)
        
        Language.query.filter_by(candidate_id=id).delete()
        for langData in data['languages']:
            lang = langData['language_name']
            level = langData['level']
            languages = Language(
                candidate_id=id,
                language_name=lang,
                level=level,
                timestamp=date_time
            )
            db.session.add(languages)

        SocialMedia.query.filter_by(candidate_id=id).delete()
        for sosmedData in data['social_media']:
            sosmedName = sosmedData['social_media_name']
            sosmedLevel = sosmedData['social_media_url']
            sosmeds = SocialMedia(
                candidate_id=id,
                social_media_name=sosmedName,
                social_media_url=sosmedLevel,
                timestamp=date_time
            )
            db.session.add(sosmeds)

        db.session.commit()
        return candidate_schema.dump(candidate)

    @jwt_required()
    def delete(self, id):
        candidate = Candidate.query.filter_by(id=id).first()
        if not candidate:
            abort(404, message="Candidate doesn't exist")

        db.session.delete(candidate)
        db.session.commit()
        return '', 204