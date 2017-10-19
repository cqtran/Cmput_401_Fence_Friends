from flask_security.forms import ConfirmRegisterForm, PasswordConfirmFormMixin, RegisterForm
from wtforms import StringField
from wtforms.validators import Required

class ExtendedConfirmRegisterForm(ConfirmRegisterForm, PasswordConfirmFormMixin):
    company_name = StringField('Company Name', [Required()])
    email = StringField('Email Address', [Required()])
    password = StringField('Password', [Required()])

class ExtendedRegisterForm(RegisterForm, PasswordConfirmFormMixin):
    company_name = StringField('Company Name', [Required()])
    email = StringField('Email Address', [Required()])
    password = StringField('Password', [Required()])