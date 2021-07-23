from flask import current_app
from app.base.models import ReleaseVersions, Requirements, Classifications, RequirementTypes


def get_project_release_versions(project_id):
    return [row.release_version_name for row in ReleaseVersions.query.filter_by(project_id=project_id).all()]


def get_project_requirements(project_id):
    return [row.requirement_name for row in Requirements.query.filter_by(parent_project=project_id).all()]


def get_requirement_types():
    return [row.type_name for row in RequirementTypes.query.all()]


def get_classification_levels():
    return [row.classification_name for row in Classifications.query.all()]
