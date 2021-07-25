

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

GRANT ALL PRIVILEGES ON DATABASE ratch_db TO ratch_user;

CREATE TABLE IF NOT EXISTS Users (
  user_id SERIAL PRIMARY KEY,
  first_name VARCHAR (32) NOT NULL,
  last_name VARCHAR (32) NOT NULL,
  email VARCHAR (64) UNIQUE NOT NULL,
  username VARCHAR (32) UNIQUE NOT NULL,
  password BYTEA NOT NULL,
  created TIMESTAMP,
  lastseen TIMESTAMP,
  authentication_token CHAR (32) UNIQUE NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS Classifications (
  classification_id SERIAL PRIMARY KEY,
  classification_name VARCHAR (32) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Projects (
  project_id SERIAL PRIMARY KEY,
  project_name VARCHAR (64) UNIQUE NOT NULL,
  project_description TEXT,
  project_welcome_message TEXT,
  classification INT references Classifications(classification_id),
  created TIMESTAMP,
  last_modified TIMESTAMP,
  created_by INT NOT NULL references Users(user_id)
);

CREATE TABLE IF NOT EXISTS RequirementTypes (
  type_id SERIAL PRIMARY KEY,
  type_name VARCHAR (32) UNIQUE NOT NULL,
  type_description TEXT
);

CREATE TABLE IF NOT EXISTS Requirements (
  requirement_id SERIAL PRIMARY KEY,
  requirement_name VARCHAR (32) UNIQUE NOT NULL,
  release_version VARCHAR (64),
  requirement_description TEXT,
  parent_project INT references Projects(project_id),
  parent_requirement INT references Requirements(requirement_id),
  requirement_type INT NOT NULL references RequirementTypes(type_id),
  classification INT references Classifications(classification_id),
  last_modified TIMESTAMP,
  created TIMESTAMP,
  last_modified_by INT NOT NULL references Users(user_id),
  created_by INT NOT NULL references Users(user_id)
);

CREATE TABLE IF NOT EXISTS TestCaseTypes (
  case_type_id SERIAL PRIMARY KEY,
  case_type_name VARCHAR (32) UNIQUE NOT NULL,
  case_type_description TEXT
);

CREATE TABLE IF NOT EXISTS TestCaseFormats (
  format_id SERIAL PRIMARY KEY,
  format_name VARCHAR (32) UNIQUE NOT NULL,
  format_description TEXT
);

CREATE TABLE IF NOT EXISTS TestCases (
  case_id SERIAL PRIMARY KEY,
  case_name VARCHAR (64),
  case_type INT references TestCaseTypes(case_type_id),
  case_format INT references TestCaseFormats(format_id),
  case_objective TEXT,
  case_overview TEXT,
  prerequisites TEXT,
  last_modified TIMESTAMP,
  last_modified_by INT NOT NULL references Users(user_id),
  created_by INT NOT NULL references Users(user_id)
);

CREATE TABLE IF NOT EXISTS TestStepTypes (
  step_type_id SERIAL PRIMARY KEY,
  step_type_name VARCHAR (32) UNIQUE NOT NULL,
  step_type_description TEXT
);

CREATE TABLE IF NOT EXISTS TestSteps (
  step_id SERIAL PRIMARY KEY,
  procedure_text TEXT,
  verification_text TEXT,
  notes TEXT,
  test_case INT NOT NULL references TestCases(case_id),
  step_number INT NOT NULL
);

CREATE TABLE IF NOT EXISTS RequirementsByTestSteps (
  step_id INT NOT NULL references TestSteps(step_id),
  requirement_id INT NOT NULL references Requirements(requirement_id),
  PRIMARY KEY(step_id, requirement_id)
);

CREATE TABLE IF NOT EXISTS TestStepsByTestCases (
  case_id INT references TestCases(case_id),
  step_id INT references TestSteps(step_id),
  PRIMARY KEY(case_id, step_id)
);

CREATE TABLE IF NOT EXISTS CustomFieldTypes (
  custom_field_type_id SERIAL PRIMARY KEY,
  custom_field_type_name VARCHAR (32) UNIQUE
);

CREATE TABLE IF NOT EXISTS CustomFields (
  custom_field_id SERIAL PRIMARY KEY,
  custom_field_name VARCHAR (32) NOT NULL,
  custom_field_description TEXT,
  custom_field_type INT NOT NULL references CustomFieldTypes(custom_field_type_id)
);

CREATE TABLE IF NOT EXISTS ReleaseVersions (
  project_id INT references Projects(project_id),
  release_version_name VARCHAR (64),
  release_version_description TEXT,
  PRIMARY KEY(project_id, release_version_name)
);

CREATE TABLE IF NOT EXISTS UsersByProject (
  user_id INT UNIQUE NOT NULL references Users(user_id),
  project_id INT NOT NULL references Projects(project_id),
  PRIMARY KEY(user_id, project_id)
);

CREATE TABLE IF NOT EXISTS RequirementsByProject (
  project_id INT NOT NULL references Projects(project_id),
  requirement_id INT NOT NULL references Requirements(requirement_id),
  PRIMARY KEY(project_id, requirement_id)
);

CREATE TABLE IF NOT EXISTS TestCasesByProject (
  project_id INT NOT NULL references Projects(project_id),
  case_id INT NOT NULL references TestCases(case_id),
  PRIMARY KEY(project_id, case_id)
);

CREATE TABLE IF NOT EXISTS Permissions (
  permission_id SERIAL PRIMARY KEY,
  permission_name VARCHAR NOT NULL,
  permission_description TEXT
);

CREATE TABLE IF NOT EXISTS ProjectRoles (
  project_role_id SERIAL PRIMARY KEY,
  project_role_name VARCHAR (32),
  project_role_description TEXT
);

CREATE TABLE IF NOT EXISTS PermissionsByProjectRole (
  project_role_id INT NOT NULL references ProjectRoles(project_role_id),
  permission_id INT NOT NULL references Permissions(permission_id),
  PRIMARY KEY(project_role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS GlobalRoles (
  global_role_id SERIAL PRIMARY KEY,
  global_role_name VARCHAR (32) NOT NULL,
  global_role_description TEXT
);

CREATE TABLE IF NOT EXISTS PermissionsByGlobalRole (
  permission_id INT NOT NULL references Permissions(permission_id),
  global_role_id INT NOT NULL references GlobalRoles(global_role_id),
  PRIMARY KEY(global_role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS GlobalRolesByUser (
  user_id INT NOT NULL references Users(user_id),
  global_role_id INT NOT NULL references GlobalRoles(global_role_id),
  grant_date TIMESTAMP,
  PRIMARY KEY (user_id, global_role_id)
);

CREATE TABLE IF NOT EXISTS ProjectRolesByUser (
  user_id INT NOT NULL references Users(user_id),
  project_role_id INT NOT NULL references ProjectRoles(project_role_id),
  grant_date TIMESTAMP,
  PRIMARY KEY(user_id, project_role_id)
);

INSERT INTO Classifications (classification_name)
VALUES
    ('Unclassified'),
    ('Unclassified//FOUO'),
    ('Confidential'),
    ('Secret'),
    ('Top Secret'),
    ('SCI'),
    ('Top Secret//SCI');

INSERT INTO RequirementTypes (type_name, type_description)
VALUES
    ('Functional', 'Describes a behavior of a system or function.'),
    ('Non-Functional', 'Describes non-functional system characteristics such as appearance.'),
    ('Constraint', 'Describes a limitation of a system characteristic or function.'),
    ('Performance', 'Describes a benchmark to which a characteristic of a function must be held.'),
    ('Specification', 'Describes in exacting detail an aspect of a system.'),
    ('Accessibility', 'Describes a function or feature related to system accessibility by users with various disabilities.');

INSERT INTO TestCaseTypes (case_type_name, case_type_description)
VALUES
    ('User Interface', 'Validates a portion of a system UI.'),
    ('Performance', 'Validates the functionality of a system under load conditions.'),
    ('Functional', 'Validates a portion of system functionality.'),
    ('Ad-hoc', 'A test which seeks to uncover bugs through system exploration.');

INSERT INTO TestCaseFormats (format_name, format_description)
VALUES
    ('Step-driven', 'The default test case style. Discreet steps with procedure, verification and notes sections.'),
    ('Free-text', 'Markdown-formatted text with no implicit discreet steps.');

INSERT INTO TestStepTypes (step_type_name, step_type_description)
VALUES
    ('Procedural', 'A standard test step, with procedure, verification, and notes sections.'),
    ('Informational', 'A note inserted by the engineer to note details or important information about upcoming steps.');

INSERT INTO GlobalRoles (global_role_name, global_role_description)
VALUES
    ('Administrator', 'Global instance administrator, with all rights to modify any project or system setting.'),
    ('User', 'Standard user, with the ability to be granted additional permissions on a per-project basis.');

INSERT INTO ProjectRoles (project_role_name, project_role_description)
VALUES
    ('Project Owner', 'Allows administration and configuration of a project, as well as the ability to add and manage users.'),
    ('Developer', 'Allows creation and modification of requirements, datasets, test cycles and test cases.'),
    ('Auditor', 'Allows read-only access to all aspects of a project.'),
    ('Test Automation', 'A robot user for executing test cycles.');

EOSQL