from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateProjectForm(FlaskForm):
    classifications = None

    project_name = TextField('Name', id='project_name',
                             validators=[DataRequired()])

    classification = SelectField(
        'Classification', id='classification', choices=classifications)

    project_description = TextAreaField('Project Description',
                                        id='project_description')

    project_welcome_message = TextAreaField('Project Welcome Message',
                                            id='project_welcome_message')
