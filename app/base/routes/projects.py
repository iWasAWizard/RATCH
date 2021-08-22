from datetime import datetime
from flask import render_template, redirect, request, url_for
from flask_login import current_user

from app.database import db
from app.base import blueprint
from app.base.forms.projects import CreateProjectForm
from app.database.models import Projects, Classifications


@blueprint.route('/create/project', methods=['GET', 'POST'])
def create_project():
    classifications = [row.classification_name for row in Classifications.query.all()]

    create_project_form = CreateProjectForm(request.form, classifications)
    if 'create' in request.form:

        project_name = request.form['project_name']

        # Check if project exists.
        project = Projects.query.filter_by(project_name=project_name).first()
        if project:
            return render_template('projects/create.html',
                                   msg="A project with that name already \
                                       exists.",
                                   success=False, form=create_project_form)

        # Else create the project.
        project = Projects(created=datetime.utcnow(),
                           last_modified=datetime.utcnow(),
                           created_by=current_user.user_id,
                           **request.form)

        db.session.add(project)
        db.session.commit()

        return render_template('projects/create.html',
                               msg='Project created!',
                               success=True,
                               form=CreateProjectForm(request.form, classifications))

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    else:
        return render_template('projects/create.html',
                               form=create_project_form)
