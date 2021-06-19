from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.base.models import (
    RequirementTypes,
    Classifications,
    Requirements,
    ReleaseVersions
)


class CreateRequirementForm(FlaskForm):
    project_id = None
    parent_choices = Requirements.get_project_requirements(project_id)
    release_versions = ReleaseVersions.get_project_release_versions(project_id)
    type_choices = RequirementTypes.get_requirement_types()
    classification_choices = Classifications.get_classification_levels()

    requirement_type = SelectField(
        'Requirement Type', id='requirement_type', choices=type_choices)

    classification = SelectField(
        'Classification', id='classification', choices=classification_choices)

    parent_requirement = SelectField('Parent Requirement',
                                     id='parent_requirement',
                                     description='The parent requirement. Leave \
                                         blank to create a root requirement.',
                                     choices=parent_choices)

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
