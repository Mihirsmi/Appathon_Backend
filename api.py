import connector
from constants import *
from flask import Flask, request, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
from controllers import questionController, userController
from models import documents, embedded_documents

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SECRET_KEY']

#Working correctly
api.add_resource(userController.UserController,'/api/users')
api.add_resource(userController.CredentialController, '/api/updatePassword')
api.add_resource(userController.LogInController, '/api/login')
api.add_resource(userController.EmailVerificationController, '/api/verifyEmail')
api.add_resource(userController.ForgotPasswordController, '/api/sendEmail')

api.add_resource(questionController.AskQuestionController, '/api/askQuestion')
api.add_resource(questionController.AnswerQuestion, '/api/answerQuestion')

@app.route('/api/forgotPassword', methods = ['GET', 'POST'])
def setNewPassword():
    import pdb; pdb.set_trace()
    if request.method == 'POST':
        token = request.args.get('token')
        user = documents.User.verify_auth_token(token)
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')

        if new_password == confirm_password and len(new_password) >= 6:
            user.encrypt_password(new_password)
            user.save()
            return 'Successfully changed your password'

        if len(new_password) < 6:
            return 'Password Length should not be less than 4'

        return 'Both Passwords do not match'
    else:
        return render_template('forgotPassword.html')

if __name__ == '__main__':
    app.run(debug=True)
