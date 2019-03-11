from enum import Enum

# noinspection PyPackageRequirements
from sqlalchemy import exists
from faker import Faker

from arctic_office_projects_api import db
from arctic_office_projects_api.main.utils import generate_neutral_id


class Project(db.Model):
    """
    Represents information about a research project
    """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    title = db.Column(db.Text(), nullable=False)

    people = db.relationship("PersonProjectRole", back_populates="project")

    def __repr__(self):
        return f"<Project { self.neutral_id }>"

    @staticmethod
    def seed(*, quantity: int = 1):
        """
        Populate database with mock/fake data

        By default, a single, static, resource will be added to allow testing against a predictable/stable instance.
        Additional instances are created randomly using Faker.

        The quantity parameter is treated as a target number of resources to add, as Faker is unaware of unique
        constraints, and may use the same values twice. Resources with duplicate values are discarded resulting in
        fewer resources being added. For example, if 250 resources are requested, only 246 may be unique.

        :type quantity: int
        :param quantity: target number of Person Sensitive resources to create
        """
        project = Project(
            neutral_id='01D5M0CFQV4M7JASW7F87SRDYB',
            title='xxx'
        )

        if not db.session.query(exists().where(Project.neutral_id == project.neutral_id)).scalar():
            db.session.add(project)

        if quantity > 1:
            faker = Faker('en_GB')

            for i in range(1, quantity):
                resource = Project(
                    neutral_id=generate_neutral_id(),
                    title=faker.sentence()
                )

                db.session.add(resource)


class Person(db.Model):
    """
    Represents information about an individual involved in research projects
    """
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    first_name = db.Column(db.Text(), nullable=False)
    last_name = db.Column(db.Text(), nullable=False)

    projects = db.relationship("PersonProjectRole", back_populates="person")

    def __repr__(self):
        return f"<Person { self.neutral_id } ({ self.last_name }, { self.first_name })>"

    @staticmethod
    def seed(*, quantity: int = 1):
        """
        Populate database with mock/fake data

        By default, a single, static, resource will be added to allow testing against a predictable/stable instance.
        Additional instances are created randomly using Faker.

        The quantity parameter is treated as a target number of resources to add, as Faker is unaware of unique
        constraints, and may use the same values twice. Resources with duplicate values are discarded resulting in
        fewer resources being added. For example, if 250 resources are requested, only 246 may be unique.

        :type quantity: int
        :param quantity: target number of Person Sensitive resources to create
        """
        person = Person(
            neutral_id='01D5MHQN3ZPH47YVSVQEVB0DAE',
            first_name='Constance',
            last_name='Watson'
        )

        if not db.session.query(exists().where(Person.neutral_id == person.neutral_id)).scalar():
            db.session.add(person)

        if quantity > 1:
            faker = Faker('en_GB')

            for i in range(1, quantity):
                resource = Person(
                    neutral_id=generate_neutral_id(),
                    first_name=faker.first_name(),
                    last_name=faker.last_name()
                )

                db.session.add(resource)


class InvestigativeRole(Enum):
    """
    Represents the terms of the 'Investigative Role' class in the Scholarly Contributions and Roles Ontology (SCoRO)

    Source: http://purl.org/spar/scoro/InvestigationRole
    """
    chief_scientist = 'Chief Scientist'
    co_investigator = 'Co Investigator'
    collaborator = 'Collaborator'
    computer_programmer = 'Computer_programmer'
    consultant = 'Consultant'
    inventor = 'Inventor'
    post_doctoral_researcher = 'Post-Doctoral Researcher'
    principal_investigator = 'Principle Investigator'
    project_student = 'Project Student'
    research_assistant = 'Research Assistant'
    research_student = 'Research Student'
    researcher = 'Researcher'
    scholar = 'Scholar'
    service_engineer = 'Service Engineer'
    technician = 'Technician'


class PersonProjectRole(db.Model):
    """
    Represents the relationship between an individual and a research project (i.e. their role)
    """
    __tablename__ = 'people_projects'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)
    investigative_role = db.Column(db.Enum(InvestigativeRole), nullable=True)

    project = db.relationship("Project", back_populates="people")
    person = db.relationship("Person", back_populates="projects")

    def __repr__(self):
        return f"<Person:Project { self.person.neutral_id }:{ self.project.neutral_id }>"

    @staticmethod
    def seed(*, quantity: int = 1):
        """
        Populate database with mock/fake data

        By default, a single, static, resource will be added to allow testing against a predictable/stable instance.
        Additional instances are created randomly using Faker.

        The quantity parameter is treated as a target number of resources to add, as Faker is unaware of unique
        constraints, and may use the same values twice. Resources with duplicate values are discarded resulting in
        fewer resources being added. For example, if 250 resources are requested, only 246 may be unique.

        :type quantity: int
        :param quantity: target number of Person Sensitive resources to create
        """
        project_nid = '01D5M0CFQV4M7JASW7F87SRDYB'
        person_nid = '01D5MHQN3ZPH47YVSVQEVB0DAE'

        if db.session.query(PersonProjectRole).filter(
            Project.neutral_id == project_nid,
            Person.neutral_id == person_nid
        ).first() is None:
            person_project = PersonProjectRole(
                project=Project.query.filter_by(neutral_id=project_nid).one(),
                person=Person.query.filter_by(neutral_id=person_nid).one(),
                investigative_role=InvestigativeRole.principal_investigator
            )
            db.session.add(person_project)

        if quantity > 1:
            pass
