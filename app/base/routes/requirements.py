from datetime import datetime
from flask import render_template, redirect, request, url_for
from flask_login import current_user

from app import db
from app.base import blueprint
from app.base.forms.requirements import CreateRequirementForm
from app.base.models import Projects, Requirements


@blueprint.route('/<project_id>/create/requirement/', methods=['GET', 'POST'])
def create_requirement(project_id):
    create_requirement_form = CreateRequirementForm(request.form)
    create_requirement_form.project_id = project_id

    project = Projects.query.filter_by(project_id=project_id).first()
    if not project:
        return render_template('not-found.html', msg=f"Project with ID \
            '{project_id}' not found!")

    if 'create' in request.form:

        req_name = request.form['requirement_name']

        # Check if a requirement with that name already exists.
        req = Requirements.query.filter_by(parent_project=project_id,
                                           requirement_name=req_name).first()

        if req:
            return render_template('requirements/create.html',
                                   msg="A requirement with that name already \
                                       exists in this project.",
                                   success=False, form=create_requirement_form)

        # Else create the requirement
        req = Requirements(created=datetime.utcnow(),
                           last_modified=datetime.utcnow(),
                           created_by=current_user.user_id,
                           last_modified_by=current_user.user_id,
                           parent_project=project_id,
                           **request.form)

        db.session.add(req)
        db.session.commit()

        return render_template('requirements/create.html',
                               msg='Requirement created!',
                               success=True,
                               form=create_requirement_form)

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    else:
        return render_template('requirements/create.html',
                               form=create_requirement_form)
