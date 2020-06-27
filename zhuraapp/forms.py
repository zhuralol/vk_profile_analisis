from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange
from zhuraapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])

    invite = StringField('Инвайт',
                        validators=[DataRequired()])

    password = PasswordField('Пароль',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Подтвердите пароль',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Имя занято, выберите другое')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Почта уже используется')

    def validate_invite(self, invite):
        print(invite)
        print(invite.data)
        if str(invite.data) == "mospolytech":
            pass
        else:
            raise ValidationError('Инвайт недействителен')


class LoginForm(FlaskForm):
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль',
                             validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class MoneyForm(FlaskForm):
    money_value = FloatField('Пополнить на',
                             validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Пополнить счет')

class UseridForm(FlaskForm):
    user_id = StringField('id пользователя',
                             validators=[DataRequired(), Length(min=1)])

    # user_id.data
    #
    # if (str(user_id.data).startswith("https://vk.com/")):
    #     user_id.data = str.replace('https://vk.com/', '')
    submit = SubmitField('анализировать')

class AnalisisForm(FlaskForm):
    user_id = StringField('id пользователя', validators=[DataRequired(), Length(min=1)])
    interests = BooleanField('Интересы')
    friend_list = BooleanField('Список друзей')
    friend_graph = BooleanField('Граф друзей')
    # user_id.data
    #
    # if (str(user_id.data).startswith("https://vk.com/")):
    #     user_id.data = str.replace('https://vk.com/', '')
    submit = SubmitField('Начать анализ')