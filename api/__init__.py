from flask_restful import Api
from app import app
from api.user import *
from api.feedback import *
from api.candidate import *
from api.job import *


restServer = Api(app)
#Auth
restServer.add_resource(UserLogin, "/api/v1.0/login")
restServer.add_resource(UserSignup, "/api/v1.0/signup")
restServer.add_resource(UserReset, "/api/v1.0/reset_password")
#User
restServer.add_resource(UserList, "/api/v1.0/user")
restServer.add_resource(UserID, "/api/v1.0/user/<int:id>")
#Candidate
restServer.add_resource(CandidateSearch, "/api/v1.0/candidate/search", endpoint='candidate')
restServer.add_resource(CandidateList, "/api/v1.0/candidate/page/<int:page>")
restServer.add_resource(CandidateID, "/api/v1.0/candidate/<int:id>")
#Job
restServer.add_resource(JobSearch, "/api/v1.0/job/search", endpoint='job')
restServer.add_resource(JobFrequently, "/api/v1.0/job/frequently")
restServer.add_resource(JobSearchCount, "/api/v1.0/job/search_count")
restServer.add_resource(JobList, "/api/v1.0/job/page/<int:page>")
restServer.add_resource(JobPost, "/api/v1.0/job")
restServer.add_resource(JobID, "/api/v1.0/job/<int:id>")
restServer.add_resource(JobViewCount, "/api/v1.0/job_count/<int:id>")
#Feedback
restServer.add_resource(FeedbackList, "/api/v1.0/feedback")
restServer.add_resource(FeedbackID, "/api/v1.0/feedback/<int:id>")