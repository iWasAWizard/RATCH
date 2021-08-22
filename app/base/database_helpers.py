from app.base.models import (
    Classifications,
    RequirementTypes,
    TestCaseTypes,
    TestCaseFormats,
    TestStepTypes,
    ProjectRoles,
    GlobalRoles
)


def seed_database():
    # Classification Levels
    for i in ['Unclassified',
              'Unclassified//FOUO',
              'CUI',
              'Confidential',
              'Secret',
              'Top Secret',
              'SCI',
              'Top Secret//SCI']:
        classification = Classifications(classification_name=i)
        db.session.add(classification)

    # Requirement Types
    for i in [('Functional',
               'Describes a behavior of a system or function.'),
              ('Non-Functional',
               'Describes non-functional system characteristics such as appearance.'),
              ('Constraint',
               'Describes a limitation of a system characteristic or function.'),
              ('Performance',
               'Describes a benchmark to which a characteristic of a function must be held.'),
              ('Specification',
               'Describes in exacting detail an aspect of a system.'),
              ('Accessibility',
               'Describes a function or feature related to system accessibility by users with various disabilities.')]:
        requirementtype = RequirementTypes(type_name=i[0], type_description=i[1])
        db.session.add(requirementtype)

    # Test Case Types
    for i in [('User Interface',
               'Validates a portion of a system UI.'),
              ('Performance',
               'Validates the functionality of a system under load conditions.'),
              ('Functional',
               'Validates a portion of system functionality.'),
              ('Ad-hoc',
               'A test which seeks to uncover bugs through system exploration.')]:
        testcasetype = TestCaseTypes(case_type_name=i[0], case_type_description=i[1])
        db.session.add(testcasetype)

    # Test Case Formats
    for i in [('Step-driven',
               'The default test case style. Discreet steps with procedure, verification and notes sections.'),
              ('Free-text',
               'Markdown-formatted text with no implicit discreet steps.')]:
        testcaseformat = TestCaseFormats(format_name=i[0], format_description=i[1])
        db.session.add(testcaseformat)

    # Test Step Types
    for i in [('Procedural',
               'A standard test step, with procedure, verification, and notes sections.'),
              ('Informational',
               'A note inserted by the engineer to note details or important information about upcoming steps.')]:
        teststeptype = TestStepTypes(step_type_name=i[0], step_type_description=i[1])
        db.session.add(teststeptype)

    # Global Roles
    for i in [('Administrator',
               'Global instance administrator, with all rights to modify any project or system setting.'),
              ('User',
               'Standard user, with the ability to be granted additional permissions on a per-project basis.')]:
        globalrole = GlobalRoles(global_role_name=i[0], global_role_description=i[1])
        db.session.add(globalrole)

    # Project Roles
    for i in [('Project Owner',
               'Allows administration and configuration of a project, as well as the ability to add and manage users.'),
              ('Developer',
               'Allows creation and modification of requirements, datasets, test cycles and test cases.'),
              ('Auditor',
               'Allows read-only access to all aspects of a project.'),
              ('Test Automation',
               'A robot user for executing test cycles.')]:
        projectrole = ProjectRoles(project_role_name=i[0], project_role_description=i[1])
        db.session.add(projectrole)

    db.session.commit()
