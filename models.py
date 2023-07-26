from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField
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
    name = db.Column(db.String(100), primary_key=True, unique=True, default='未填')
    email = db.Column(db.String(120), unique=True, default='未填')
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


class Schools(db.Model):
    __bind_key__ = 'database'
    __tablename__ = 'hetouce'

    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(255))
    specialityi = db.Column(db.String(255))
    Schoolid = db.Column(db.Integer)
    school = db.Column(db.String(255))
    plannum_2023 = db.Column(db.Integer)
    lowest_rank2023 = db.Column(db.Integer)
    lowest_rank2022 = db.Column(db.Integer)
    plannum_2022 = db.Column(db.Integer)
    lowest_rank2021 = db.Column(db.Integer)
    plannum_2021 = db.Column(db.Integer)
    forelowest_rank = db.Column(db.Integer)
    Type = db.Column(db.String(255))
    mustspe = db.Column(db.String(255), default='无限制')
    department = db.Column(db.String(255))
    locality = db.Column(db.String(255))
    feature = db.Column(db.String(255))
    probability = db.Column(db.Integer)

