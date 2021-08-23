from flask import json
from flask_login import UserMixin
from sqlalchemy import (
    LargeBinary,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import synonym
from sqlalchemy.orm.attributes import QueryableAttribute
from app.database import db
from app.base.login_manager import login_manager, hash_pass


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        kwargs['_force'] = True
        self.from_dict(**kwargs)

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model"""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, '_hidden_fields') else []
        default = self._default_fields if hasattr(self, '_default_fields') else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split('.', 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != '.':
                    item = f'.{item}'
                item = f'{_path}{item}'
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith('_'):
                continue
            check = f'{_path}.{key}'
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith('_'):
                continue
            check = f'{_path}.{key}'
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, 'all'):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=f'{_path}.{key.lower()}',
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=f'{_path}.{key.lower()}',
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = f'{_path}.{key}'
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, 'to_dict'):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=f'{_path}.{key.lower()}',
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data

    def from_dict(self, **kwargs):
        """Update this model with a dictionary"""

        _force = kwargs.pop('_force', False)

        readonly = self._readonly_fields if hasattr(self, '_readonly_fields') else []
        if hasattr(self, '_hidden_fields'):
            readonly += self._hidden_fields

        readonly += ['id', 'created_at', 'modified_at']

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        changes = {}

        for key in columns:
            if key.startswith('_'):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if val != kwargs[key]:
                    changes[key] = {'old': val, 'new': kwargs[key]}
                    setattr(self, key, kwargs[key])

        for rel in relationships:
            if key.startswith('_'):
                continue
            allowed = True if _force or rel not in readonly else False
            exists = True if rel in kwargs else False
            if allowed and exists:
                is_list = self.__mapper__.relationships[rel].uselist
                if is_list:
                    valid_ids = []
                    query = getattr(self, rel)
                    cls = self.__mapper__.relationships[rel].entity.class_
                    for item in kwargs[rel]:
                        if (
                            'id' in item
                            and query.filter_by(id=item['id']).limit(1).count() == 1
                        ):
                            obj = cls.query.filter_by(id=item['id']).first()
                            col_changes = obj.from_dict(**item)
                            if col_changes:
                                col_changes['id'] = str(item['id'])
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(item['id']))
                        else:
                            col = cls()
                            col_changes = col.from_dict(**item)
                            query.append(col)
                            db.session.flush()
                            if col_changes:
                                col_changes['id'] = str(col.id)
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(col.id))

                    # delete rows from relationship that were not in kwargs[rel]
                    for item in query.filter(not(cls.id.in_(valid_ids))).all():
                        col_changes = {'id': str(item.id), 'deleted': True}
                        if rel in changes:
                            changes[rel].append(col_changes)
                        else:
                            changes.update({rel: [col_changes]})
                        db.session.delete(item)

                else:
                    val = getattr(self, rel)
                    if self.__mapper__.relationships[rel].query_class is not None:
                        if val is not None:
                            col_changes = val.from_dict(**kwargs[rel])
                            if col_changes:
                                changes.update({rel: col_changes})
                    else:
                        if val != kwargs[rel]:
                            setattr(self, rel, kwargs[rel])
                            changes[rel] = {'old': val, 'new': kwargs[rel]}

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, 'to_dict'):
                    val = val.to_dict()
                changes[key] = {'old': val, 'new': kwargs[key]}
                setattr(self, key, kwargs[key])

        return changes


class Users(BaseModel, UserMixin):
    """Table of user object data"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32))
    password = Column(LargeBinary)
    created = Column(DateTime)
    last_seen = Column(DateTime)
    notes = Column(Text)
    authentication_token = Column(String, unique=True, nullable=False)

    id = synonym('user_id')

    _default_fields = [
        'user_id',
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    _hidden_fields = [
        'password',
        'notes',
        'authentication_token',
    ]
    _readonly_fields = [
        'created',
        'last_seen',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                # Password is stored in the database as a bytes object, so this gets that.
                value = hash_pass(value)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    return user if user else None


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class Classifications(BaseModel):
    """Table of classification levels that can be mapped to project and requirement objects"""
    __tablename__ = 'classifications'

    classification_id = Column(Integer, primary_key=True)
    classification_name = Column(String(32), unique=True, nullable=False)

    id = synonym('classification_id')

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.classification_name)


class RequirementTypes(BaseModel):
    """Table of types that can be mapped to requirement objects"""
    __tablename__ = 'requirementtypes'

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String(32), unique=True, nullable=False)
    type_description = Column(Text)

    id = synonym('type_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.type_name)


class Requirements(BaseModel):
    """Table of requirements that have been created for all projects and their data"""
    __tablename__ = 'requirements'

    requirement_id = Column(Integer, primary_key=True)
    requirement_name = Column(String(32), unique=True, nullable=False)
    release_version = Column(String(64))
    requirement_description = Column(Text)
    parent_project = Column(Integer, ForeignKey('projects.project_id'))
    parent_requirement = Column(
        Integer, ForeignKey('requirements.requirement_id'))
    requirement_type = Column(Integer, ForeignKey('requirementtypes.type_id'))
    classification = Column(Integer, ForeignKey(
        'classifications.classification_id'))
    created = Column(DateTime)
    last_modified = Column(DateTime)
    last_modified_by = Column(Integer, ForeignKey('users.user_id'))
    created_by = Column(Integer, ForeignKey('users.user_id'))

    id = synonym('requirement_id')

    _default_fields = [
        'requirement_id',
        'requirement_name',
        'release_version',
        'requirement_description',
        'parent_project',
        'parent_requirement',
        'requirement_type',
        'classification',
    ]
    _hidden_fields = []
    _readonly_fields = [
        'created',
        'last_modified',
        'last_modified_by',
        'created_by',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'classification':
                value = Classifications.query.filter_by(
                    classification_name=value).first().classification_id

            setattr(self, property, value)

    def __repr__(self):
        return str(self.requirement_name)


class TestCaseFormats(BaseModel):
    """Table of formats that can be mapped to test cases"""
    __tablename__ = 'testcaseformats'

    format_id = Column(Integer, primary_key=True)
    format_name = Column(String(32), unique=True, nullable=True)
    format_description = Column(Text)

    id = synonym('format_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.format_name)


class TestCaseTypes(BaseModel):
    """Table of types that can be mapped to test cases"""
    __tablename__ = 'testcasetypes'

    case_type_id = Column(Integer, primary_key=True)
    case_type_name = Column(String(32), unique=True, nullable=False)
    case_type_description = Column(Text)

    id = synonym('case_type_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.case_type_name)


class TestCases(BaseModel):
    """Table of test cases that have been created for all projects"""
    __tablename__ = 'testcases'

    case_id = Column(Integer, primary_key=True)
    case_name = Column(String(64), unique=True, nullable=False)
    case_type = Column(Integer, ForeignKey('testcasetypes.case_type_id'))
    case_format = Column(Integer, ForeignKey('testcaseformats.format_id'))
    case_objective = Column(Text)
    case_overview = Column(Text)
    prerequisites = Column(Text)
    created = Column(DateTime)
    last_modified = Column(DateTime)
    last_modified_by = Column(Integer, ForeignKey('users.user_id'))
    created_by = Column(Integer, ForeignKey('users.user_id'))

    id = synonym('case_id')

    _default_fields = [
        'case_id',
        'case_name',
        'case_type',
        'case_format',
        'case_objective',
        'case_overview',
        'prerequisites',
    ]
    _hidden_fields = []
    _readonly_fields = [
        'created',
        'last_modified',
        'last_modified_by',
        'created_by',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.case_name)


class TestStepTypes(BaseModel):
    """Table of types that can be assigned to test cases"""
    __tablename__ = 'teststeptypes'

    step_type_id = Column(Integer, primary_key=True)
    step_type_name = Column(String(32), unique=True, nullable=False)
    step_type_description = Column(Text)

    id = synonym('step_type_id')

    def __init__(self, **kwargs):
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.step_type_name)


class TestSteps(BaseModel):
    """Table of all test steps for all test cases"""
    __tablename__ = 'teststeps'

    step_id = Column(Integer, primary_key=True)
    procedure_text = Column(Text)
    verification_text = Column(Text)
    notes = Column(Text)
    test_case = Column(Integer, ForeignKey('testcases.case_id'))
    step_number = Column(Integer)

    id = synonym('step_id')

    _default_fields = [
        'step_id',
        'procedure_text',
        'verification_text',
        'test_case',
        'step_number',
        'parent_requirement',
        'requirement_type',
        'classification',
    ]
    _hidden_fields = []
    _readonly_fields = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.step_id)


class Projects(BaseModel):
    """Table of project data"""
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(32), unique=True, nullable=False)
    project_description = Column(Text)
    project_welcome_message = Column(Text)
    classification = Column(Integer, ForeignKey(
        'classifications.classification_id'))
    created = Column(DateTime)
    last_modified = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.user_id'))

    id = synonym('project_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'classification':
                value = Classifications.query.filter_by(
                    classification_name=value).first().classification_id

            setattr(self, property, value)

    def __repr__(self):
        return str(self.project_name)


class ReleaseVersions(BaseModel):
    """Table of release versions that have been created for all projects"""
    __tablename__ = 'releaseversions'

    project_id = Column(Integer, ForeignKey(
        'projects.project_id'), primary_key=True)
    release_version_name = Column(String(64), nullable=False, primary_key=True)
    release_version_description = Column(Text)

    id = synonym('project_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.release_version_name)


class Permissions(BaseModel):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(String(64), nullable=False)
    permission_description = Column(Text)

    id = synonym('permission_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.permission_name)


class ProjectRoles(BaseModel):
    __tablename__ = 'projectroles'

    project_role_id = Column(Integer, primary_key=True)
    project_role_name = Column(String(32), nullable=False)
    project_role_description = Column(Text)

    id = synonym('project_role_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.project_role_name)


class GlobalRoles(BaseModel):
    __tablename__ = 'globalroles'

    global_role_id = Column(Integer, primary_key=True)
    global_role_name = Column(String(32), nullable=False)
    global_role_description = Column(Text)

    id = synonym('global_role_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Iterate over the properties of a request
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.global_role_name)
