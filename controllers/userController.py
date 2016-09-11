from __init__ import *
from auth import auth
from util import *

class LogInController(Resource):

    #@auth.login_required
    def get(self):
        #Extra code
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Please specify username')
        parser.add_argument('password', required=True, help='Please specify password')
        args = parser.parse_args()
        #End Extra code
        response = {}
        response['id'] = str(g.user.id)
        response['username'] = g.user.username
        response['email'] = g.user.email
        response['token'] = g.user.generate_auth_token()
        return response


class UserController(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Please specify email')
        parser.add_argument('username', required=True, help='Please specify username')
        parser.add_argument('password', required=True, help='Please specify password')

        args = parser.parse_args()

        if(len(args['password']) < 6 and len(args['password']) > 32):
            return {'response':'Length of password'},403

        user = documents.User()
        user.email = args['email']
        user.username = args['username']
        user.encrypt_password(args['password'])

        try:
            user.save()
            sendEmail(user.generate_auth_token(),args['email'])
        except Exception as e:
            return{'response':'Invalid email or objectId for user'},400
        userInfo = {}
        userInfo['id'] = str(user.id)
        userInfo['email'] = user.email
        userInfo['username'] = user.username

        return userInfo

class CredentialController(Resource):

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('old_password', required=True, help='Please specify old password')
        parser.add_argument('new_password', required=True, help='Please specify new password')
        args = parser.parse_args()

        if(g.user.verify_password(args['old_password'])):
            g.user.encrypt_password(args['new_password'])
            g.user.save()
            return {'response':'Success'}

        return {'response':'Unauthorized'},401

class EmailVerificationController(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Please specify token for Verification')
        args = parser.parse_args()
        userVerified = documents.User.verify_auth_token(args['token'])
        if userVerified is None:
            return {'response':'Try Again'},403
        userVerified.isEmailConfirmed = True
        userVerified.save()
        return {'response':'Verified'}

class ForgotPasswordController(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Please specify email')
        args = parser.parse_args()
        user = documents.User.objects(email=args['email']).first()
        if user is None:
            return {'response':'No user found'},400
        sendPasswordEmail(user.generate_auth_token(), args['email'])
        return {'response':'Link sent Successfully'}
