from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired
from app.base.models import (
    RequirementTypes,
    Classifications,
    Requirements,
    ReleaseVersions
)


class CreateTestCaseForm(FlaskForm):
    pass
