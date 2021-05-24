#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

GRANT ALL PRIVILEGES ON DATABASE ratch_db TO ratch_user;

CREATE EXTENSION pgcrypto;

CREATE TABLE IF NOT EXISTS Users (
  user_id SERIAL PRIMARY KEY,
  first_name VARCHAR (32)NOT NULL,
  last_name VARCHAR (32) NOT NULL,
  email VARCHAR (64) UNIQUE NOT NULL,
  username VARCHAR (16) UNIQUE NOT NULL,
  password VARCHAR (32) NOT NULL,
  created TIMESTAMP,
  lastseen TIMESTAMP,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS RequirementTypes (
  type_id SERIAL PRIMARY KEY,
  type_name VARCHAR (32) UNIQUE NOT NULL,
  type_description TEXT
);

CREATE TABLE IF NOT EXISTS Requirements (
  requirement_id SERIAL PRIMARY KEY,
  requirement_name VARCHAR (32),
  release_version VARCHAR (64),
  requirement_desciption TEXT,
  type INT NOT NULL references RequirementTypes(type_id),
  classification VARCHAR (32),
  last_modified TIMESTAMP,
  last_modified_by INT NOT NULL references Users(user_id)
);

CREATE TABLE IF NOT EXISTS TestCases (
  case_id SERIAL PRIMARY KEY,
  case_name VARCHAR (64),
  case_description TEXT,
  prerequisites TEXT,
  last_modified TIMESTAMP,
  last_modified_by INT NOT NULL references Users(user_id)
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

CREATE TABLE IF NOT EXISTS Projects (
  project_id SERIAL PRIMARY KEY,
  project_name VARCHAR (64) UNIQUE NOT NULL,
  project_description TEXT,
  classification VARCHAR (32),
  created TIMESTAMP,
  updated TIMESTAMP
);

CREATE TABLE IF NOT EXISTS UsersByProject (
  user_id INT UNIQUE NOT NULL references Users(user_id),
  project_id INT NOT NULL references Projects(project_id)
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
  project_id INT NOT NULL references Projects(project_id),
  description TEXT
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

CREATE TABLE IF NOT EXISTS ProjectRoles (
  project_role_id SERIAL PRIMARY KEY,
  project_role_name VARCHAR (32) NOT NULL,
  project_role_description TEXT
);

CREATE TABLE IF NOT EXISTS PermissionByProjectRole (
  project_role_id INT NOT NULL references ProjectRoles(project_role_id),
  permission_id INT NOT NULL references Permissions(permission_id),
  PRIMARY KEY(project_role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS GlobalRoleByUser (
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

EOSQL