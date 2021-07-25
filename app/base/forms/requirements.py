from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateRequirementForm(FlaskForm):
    project_id = None
    release_versions = None
    reqtypes = None
    classifications = None
    requirements = None

    requirement_type = SelectField(
        'Requirement Type', id='requirement_type', choices=reqtypes)

    classification = SelectField(
        'Classification', id='classification', choices=classifications)

    parent_requirement = SelectField('Parent Requirement',
                                     id='parent_requirement',
                                     description='The parent requirement. Leave \
                                         blank to create a root requirement.',
                                     choices=requirements)

    requirement_name = TextField('Name', id='requirement_name',
                                 validators=[DataRequired()])

    release_version = SelectField(id='release_version',
                                  description='The project release version in \
                                      which this requirement is to be \
                                      implemented.',
                                  choices=release_versions)

    requirement_description = TextAreaField('Requirement Body',
                                            id='requirement_description',
                                            validators=[DataRequired()])
