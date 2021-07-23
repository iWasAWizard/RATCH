from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.base.db_utils import get_classification_levels


class CreateProjectForm(FlaskForm):
    classification_choices = get_classification_levels()

    project_name = TextField('Name', id='project_name',
                             validators=[DataRequired()])

    classification = SelectField(
        'Classification', id='classification', choices=classification_choices)

    project_description = TextAreaField('Project Description',
                                        id='project_description')

    project_welcome_message = TextAreaField('Project Welcome Message',
                                            id='project_welcome_message')
