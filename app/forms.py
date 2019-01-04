from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UpdateEmailForm(FlaskForm):
    current_email = StringField('Current Email', validators = [DataRequired(), Email()])
    # if current_email != current_user_email:
    #    raise ValidationError('Incorrect Current Email!')
    new_email = StringField('New Email', validators = [DataRequired(), Email()])
    new_email2 = StringField('Confirm New Email', validators = [DataRequired(), Email(), EqualTo('new_email')])
    #if new_email2 != new_email:
     #   raise ValidationError('New emails do not match!')
    submit = SubmitField('Update Email')
    #if submit.validate_on_submit():
    #    raise ValidationError('Email succesfully updated!')
   # flash('An error occured while updateing your email.')
   # return redirect(url_for('update_email'))


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators = [DataRequired()])
    #if not check_password_hash(current_user.password_hash, current_password):
     #   raise ValidationError('This is not the correct current password')
       # return redirect(url_for('index'))
    new_password = PasswordField('New Password', validators = [DataRequired()])
    new_password2 = PasswordField('Confirm New Password', validators = [DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')
   # if submit.validate_on_submit():
   #     raise ValidationError('Password Succesfully Updated!')
       # return redirect(url_for('index'))
   # flash('An error occured while updating password')
   # return redirect(url_for('index'))

class SettingsForm(FlaskForm):
    pass
