from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 定义注册表单类
class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')


# 定义登录表单类
class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, default='0')
    name = db.Column(db.String(100), default='未填')
    email = db.Column(db.String(120), unique=True, default='未填')
    gender = db.Column(db.String(10), default='未填')
    score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)
    password = db.Column(db.String(128), default='未填')
    subject1 = db.Column(db.String(100), default='未填')
    subject2 = db.Column(db.String(100), default='未填')
    subject3 = db.Column(db.String(100), default='未填')

    def __repr__(self):
        return f"<User {self.name}>"

    def check_password(self, password):
        return self.password == password

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter(email=email).first()


class School(db.Model):
    __bind_key__ = 'database'
    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(200))
    school = db.Column(db.String(200))
    plan_number = db.Column(db.Integer)
    lowest_rank = db.Column(db.Integer)

    def __repr__(self):
        return f"<School {self.name}>"
