from flask_security.forms import ConfirmRegisterForm, PasswordConfirmFormMixin
from wtforms import StringField
from wtforms.validators import Required

class ExtendedConfirmRegisterForm(ConfirmRegisterForm, PasswordConfirmFormMixin):
    username = StringField('Company Name', [Required()])
    email = StringField('Email Address', [Required()])
    password = StringField('Password', [Required()])