import enum

from sql_alchemy import db


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class UserModel(db.Model):
    __tablename__ = 'usuarios'

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30))
    senha = db.Column(db.String(30))
    role = db.Column(db.Enum(Role))

    def __init__(self, login, senha, role):
        self.login = login
        self.senha = senha
        self.role = role

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'role': self.role.value
        }

    @classmethod
    def find_by_login(cls, login):
        log = cls.query.filter_by(login=login).first()
        if log:
            return log
        return None

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
