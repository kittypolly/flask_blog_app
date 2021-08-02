from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

#아이디랑 비밀번호를 전달 받을 거에요.
#validators는 유효성 검사입니다.
#그 안에 DataRequired는 빈데이터가 없게 만드는 것이고, length 와 email등으로 형식을 검사합니다.
#password는 특별한 방식의 validator를 사용할 것입니다.

class RegistrationForm(FlaskForm):
    username = StringField('별명',
    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('암호', 
    validators=[DataRequired()])
    confirm_password = PasswordField('암호 확인', 
    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('회원가입')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('너무 짧거나 이미 있는 별명이에요.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('이미 있는 이메일이에요. 다른 이메일로 시도해주세요.')
         

class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('암호', validators=[DataRequired()])
    remember = BooleanField('로그인 정보저장')
    submit = SubmitField('로그인')

#remeber은 쿠키 같은 거다.

class UpdateAccountForm(FlaskForm):
    username = StringField('별명',
    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    #FileField는 flask 모듈에 있는거고 'Update Profile Picture는 lable을 해준거야.
    picture = FileField('프로필 사진 올리기', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('고치기')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError('너무 짧거나 이미 있는 별명이에요.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('이미 있는 이메일이에요. 다른 이메일로 시도해주세요.')    

class PostForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    submit = SubmitField('발행')
    
    
     

    
