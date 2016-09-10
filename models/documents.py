from __init__ import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeSerializer
from constants import *
from embedded_documents import *
from datetime import *

class User(DynamicDocument):
    username = StringField(unique=True)
    email = StringField(unique=True)
    password = StringField()
    isEmailConfirmed = BooleanField(default=False)

    def encrypt_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self):
        s = URLSafeSerializer(SECRET_KEY)
        return s.dumps(str(self.id))

    @staticmethod
    def verify_auth_token(token):
        s = URLSafeSerializer(SECRET_KEY)
        try:
            data = s.loads(token)
            return User.objects(id=data).first()
        except Exception as ex:
            print ex
            return None

class Question(DynamicDocument):
    question = StringField()
    questionUser = ReferenceField(User, reverse_delete_rule=CASCADE)
    answers = ListField(EmbeddedDocumentField(Answer),default=[])
