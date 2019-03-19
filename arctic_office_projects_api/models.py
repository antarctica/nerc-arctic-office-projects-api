from datetime import date
from enum import Enum

# noinspection PyPackageRequirements
from psycopg2.extras import DateRange
# noinspection PyPackageRequirements
from sqlalchemy import exists
from faker import Faker
# noinspection PyPackageRequirements
from sqlalchemy.dialects import postgresql

from arctic_office_projects_api import db
from arctic_office_projects_api.main.utils import generate_neutral_id
from arctic_office_projects_api.main.faker.providers.project import Provider as ProjectProvider
from arctic_office_projects_api.main.faker.providers.person import Provider as PersonProvider
from arctic_office_projects_api.main.faker.providers.profile import Provider as ProfileProvider

faker = Faker('en_GB')
faker.add_provider(ProjectProvider)
faker.add_provider(PersonProvider)
faker.add_provider(ProfileProvider)


class Project(db.Model):
    """
    Represents information about a research project
    """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    title = db.Column(db.Text(), nullable=False)
    acronym = db.Column(db.Text(), nullable=True)
    abstract = db.Column(db.Text(), nullable=True)
    website = db.Column(db.Text(), nullable=True)
    publications = db.Column(postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True)
    access_duration = db.Column(postgresql.DATERANGE(), nullable=False)
    project_duration = db.Column(postgresql.DATERANGE(), nullable=True)

    participants = db.relationship("Participant", back_populates="project")

    def __repr__(self):
        return f"<Project { self.neutral_id }>"

    def seed(self, *, quantity: int = 1):
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
        project_duration = DateRange(date(2013, 3, 1), date(2016, 10, 1))

        if not db.session.query(exists().where(Project.neutral_id == project_nid)).scalar():
            project = Project(
                neutral_id=project_nid,
                title='Aerosol-Cloud Coupling And Climate Interactions in the Arctic',
                acronym='ACCACIA',
                abstract="The Arctic climate is changing twice as fast as the global average and these dramatic "
                         "changes are evident in the decreases in sea ice extent over the last few decades. The "
                         "lowest sea ice cover to date was recorded in 2007 and recent data suggests sea ice cover "
                         "this year may be even lower. Clouds play a major role in the Arctic climate and therefore "
                         "influence the extent of sea ice, but our understanding of these clouds is very poor. Low "
                         "level, visually thick, clouds in much of the world tend to have a cooling effect, because "
                         "they reflect sunlight back into space that would otherwise be absorbed at the surface. "
                         "However, in the Arctic this albedo effect is not as important because the surface, often "
                         "being covered in snow and ice, is already highly reflective and Arctic clouds therefore "
                         "tend to warm instead of cooling. Warming in the Arctic can, in turn, lead to sea ice "
                         "break-up which exposes dark underlying sea water. The sea water absorbs more of the sun's "
                         "energy, thus amplifying the original warming. Hence, small changes in cloud properties or "
                         "coverage can lead to dramatic changes in the Arctic climate; this is where the proposed "
                         "research project comes in. \n A large portion of clouds, including those found in the Arctic "
                         "region, are categorized as mixed phase clouds. This means they contain both supercooled "
                         "water droplets and ice crystals (for a demonstration of supercooled water see: "
                         "http://www.youtube.com/watch?v=0JtBZGXd5zo). Liquid cloud droplets can exist in a "
                         "supercooled state well below zero degrees centigrade without freezing. Freezing will, "
                         "however, be observed if the droplets contain a particle known as an ice nucleus that can "
                         "catalyze ice formation and growth. Ice formation dramatically alters a cloud's properties "
                         "and therefore its influence on climate. At lower latitudes, ice nuclei are typically made up "
                         "of desert dusts, soot or even bacteria. But the composition and source of ice nuclei in the "
                         "Arctic environment remains a mystery. \n A likely source of ice nuclei in the Arctic is the "
                         "ocean. Particles emitted at the sea surface, through the action of waves breaking and bubble "
                         "bursting, may serve as ice nuclei when they are lofted into the atmosphere and are "
                         "incorporated in cloud droplets. This source of ice nuclei has not yet been quantified. We "
                         "will be the first to make measurements of ice nuclei in the central Arctic region. We will "
                         "make measurements of ice nuclei in the surface layers of the sea from a research ship as "
                         "well as measuring airborne ice nuclei from the BAe-146 research aircraft. \n The sea's "
                         "surface contains a wide range of bacteria, viruses, plankton and other materials which are "
                         "ejected into the atmosphere and may cause ice to form. We will use state-of-the-art "
                         "equipment developed at Leeds to measure how well sea-derived particles and particles sampled "
                         "in the atmosphere nucleate ice. We will piggy back on a NERC funded project called ACACCIA, "
                         "which not only represents excellent value for money (since the ship and aircraft are already "
                         "paid for under ACCACIA), but is a unique opportunity to access this remote region. \n "
                         "Results from the proposed study will build upon previous work performed in the Murray "
                         "laboratory and generate quantitative results that can be directly used to improve "
                         "computer-based cloud, aerosol and climate models. Our results will further our "
                         "understanding of these mysterious and important mixed phase clouds and, in turn, the global "
                         "climate.",
                website='http://arp.arctic.ac.uk/projects/aerosol-cloud-coupling-and-climate-interactions-ar/',
                publications=[
                    'https://doi.org/10.5194/acp-2018-283',
                    'https://doi.org/10.5194/acp-15-3719-2015',
                    'https://doi.org/10.5194/acp-15-5599-2015',
                    'https://doi.org/10.5194/acp-16-4063-2016'
                ],
                access_duration=DateRange(project_duration.lower, None),
                project_duration=project_duration
            )
            db.session.add(project)

        if quantity > 1:
            for i in range(1, quantity):
                project_type = faker.project_type()
                project_duration = faker.project_duration(project_type)
                resource = Project(
                    neutral_id=generate_neutral_id(),
                    title=faker.title(),
                    abstract=faker.abstract(),
                    access_duration=DateRange(project_duration.lower, None),
                    project_duration=project_duration
                )
                if faker.has_acronym(project_type):
                    resource.acronym = faker.acronym()
                if faker.has_website(project_type):
                    resource.website = faker.uri()
                if faker.has_publications:
                    resource.publications = faker.publications_list()

                db.session.add(resource)


class Person(db.Model):
    """
    Represents information about an individual involved in research projects
    """
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    first_name = db.Column(db.Text(), nullable=True)
    last_name = db.Column(db.Text(), nullable=True)
    orcid_id = db.Column(db.String(64), unique=True, nullable=True)
    logo_url = db.Column(db.Text(), nullable=True)

    participation = db.relationship("Participant", back_populates="person")

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
        person_nid = '01D5MHQN3ZPH47YVSVQEVB0DAE'

        if not db.session.query(exists().where(Person.neutral_id == person_nid)).scalar():
            person = Person(
                neutral_id=person_nid,
                first_name='Constance',
                last_name='Watson',
                orcid_id='https://sandbox.orcid.org/0000-0001-8373-6934',
                logo_url='https://cdn.web.bas.ac.uk/bas-registers-service/v1/sample-avatars/conwat/conwat-256.jpg'
            )
            db.session.add(person)

        if quantity > 1:
            for i in range(1, quantity):
                resource = Person(neutral_id=generate_neutral_id())
                if faker.has_orcid_id():
                    resource.orcid_id = faker.orcid_id()
                if faker.male_or_female() == 'male':
                    resource.first_name = faker.first_name_male(),
                    resource.last_name = faker.last_name_male()
                    if faker.has_avatar():
                        resource.logo_url = faker.avatar_male()
                else:
                    resource.first_name = faker.first_name_female(),
                    resource.last_name = faker.last_name_female()
                    if faker.has_avatar():
                        resource.logo_url = faker.avatar_female()

                db.session.add(resource)


class ParticipantRole(Enum):
    """
    Represents the members of the various role classes in the Scholarly Contributions and Roles Ontology (SCoRO)
    """
    AuthorshipRole_ArticleGuarantor = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/article-guarantor',
        'title': 'article guarantor',
        'description': 'A person who takes responsibility for the integrity of the article as a whole, from the '
                       'inception of the research investigation to the published research article.'
    }
    AuthorshipRole_Author = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/pro/author',
        'title': 'author',
        'description': 'A person who has authorship of the work.'
    }
    AuthorshipRole_ConsortiumAuthor = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/consortium-author',
        'title': 'consortium author',
        'description': 'An organisation or consortium that has contributed collectively to the work and is named in '
                       'the list of authors.'
    }
    AuthorshipRole_CorrespondingAuthor = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/corresponding-author',
        'title': 'corresponding author',
        'description': 'An author of the work with whom editors and readers should correspond concerning it.'
    }
    AuthorshipRole_Illustrator = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/illustrator',
        'title': 'illustrator',
        'description': 'A illustrator of, or for, the work.'
    }
    AuthorshipRole_Photographer = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/photographer',
        'title': 'photographer',
        'description': 'A photographer of, or for, the work.'
    }
    AuthorshipRole_PrincipalAuthor = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/principal-author',
        'title': 'principal author',
        'description': 'An author of the work considered to have contributed most.'
    }
    AuthorshipRole_SeniorAuthor = {
        'class': 'http://purl.org/spar/scoro/AuthorshipRole',
        'member': 'http://purl.org/spar/scoro/senior-author',
        'title': 'senior author',
        'description': 'A senior author of the work.'
    }
    DataRole_AccessProvider = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/access-provider',
        'title': 'access provider',
        'description': 'An agent who provides access to a resource.'
    }
    DataRole_Curator = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/curator',
        'title': 'curator',
        'description': 'An agent who documents, cares for and manages collections of resources.'
    }
    DataRole_DataCreator = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/data-creator',
        'title': 'data creator',
        'description': 'A person who creates, originates, gathers or collects new data.'
    }
    DataRole_DataCurator = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/data-curator',
        'title': 'data curator',
        'description': 'A person who is responsible for reviewing, enhancing, cleaning, or standardizing data and '
                       'their associated metadata for their long-term preservation.'
    }
    DataRole_DataManager = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/data-manager',
        'title': 'data manager',
        'description': 'A person who is responsible for day-to-day management, maintenance and back-up of data.'
    }
    DataRole_DataPublisher = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/data-publisher',
        'title': 'data publisher',
        'description': 'An agent who publishes data.'
    }
    DataRole_DataUser = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/data-user',
        'title': 'data user',
        'description': 'A person who uses or re-uses existing data.'
    }
    DataRole_EmbargoController = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/embargo-controller',
        'title': 'embargo controller',
        'description': 'A person who has responsibility for setting and lifting embargos that restrict access to a '
                       'dataset (or other resource) for a specified period of time.'
    }
    DataRole_RepositoryManager = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/repository-manager',
        'title': 'repository manager',
        'description': 'A person who managers a repository where resources are given secure long-term storage.'
    }
    DataRole_WebMaster = {
        'class': 'http://purl.org/spar/scoro/DataRole',
        'member': 'http://purl.org/spar/scoro/web-master',
        'title': 'web master',
        'description': 'A person who has responsibility for maintaining a web site and its content.'
    }
    FinancialRole_Accountant = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/accountant ',
        'title': 'accountant ',
        'description': 'A person who has responsibility for managing financial accounts.'
    }
    FinancialRole_Auditor = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/auditor',
        'title': 'auditor',
        'description': 'A person who has responsibility for conducting formal audits of financial accounts.'
    }
    FinancialRole_Claimant = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/claimant',
        'title': 'claimant',
        'description': 'A person making a financial claim, such as for expenses.'
    }
    FinancialRole_Contractor = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/',
        'title': 'Contractor',
        'description': 'An agent who enters into a contract to undertake specified work or to supply specified '
                       'services in return for payment.'
    }
    FinancialRole_FinancialController = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/financial-controller',
        'title': 'financial controller',
        'description': 'An agent with responsibility for controlling a budget, including authorising expenditure.'
    }
    FinancialRole_Funder = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/funder',
        'title': 'funder',
        'description': 'An agent that provides funds, such as for a research project.'
    }
    FinancialRole_FundingRecipient = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/funding-recipient',
        'title': 'funding recipient',
        'description': 'An agent who is the official recipient of funding, for example the university at which the '
                       'funded research project leader is a member.'
    }
    FinancialRole_Owner = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/owner',
        'title': 'owner',
        'description': 'An agent that owns something with actual or potential financial value.'
    }
    FinancialRole_Purchaser = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/purchaser',
        'title': 'purchaser',
        'description': 'An agent with responsibility for making purchases of goods or services from a budget.'
    }
    FinancialRole_Sponsor = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/sponsor',
        'title': 'sponsor',
        'description': 'An agent that provides funds or support to an agent or endeavour, often in return for access '
                       'to the exploitable commercial potential, or endeavour\'s output.'
    }
    FinancialRole_SubContractor = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/sub-contractor',
        'title': 'sub-contractor',
        'description': 'An agent who enters into a contract to take over part of another contractor\'s obligation.'
    }
    FinancialRole_Supplier = {
        'class': 'http://purl.org/spar/scoro/FinancialRole',
        'member': 'http://purl.org/spar/scoro/supplier',
        'title': 'supplier',
        'description': 'An agent with responsibility to provide goods or services in exchange for payment.'
    }
    InvestigationRole_ChiefScientist = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/chief-scientist',
        'title': 'chief scientist',
        'description': 'The scientist who leads a research group or organization.'
    }
    InvestigationRole_CoInvestigator = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/co-investigator',
        'title': 'co-investigator',
        'description': 'A co-investigator of the research project.'
    }
    InvestigationRole_Collaborator = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/collaborator',
        'title': 'Collaborator',
        'description': 'A person, typically from another group or institution, who collaborates with those undertaking '
                       'a research project.'
    }
    InvestigationRole_ComputerProgrammer = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/computer-programmer',
        'title': 'computer programmer',
        'description': 'A person who develops computer software for a research project'
    }
    InvestigationRole_Consultant = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/consultant',
        'title': 'consultant',
        'description': 'A person who provides expertise or services for a research project'
    }
    InvestigationRole_Inventor = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/inventor',
        'title': 'inventor',
        'description': 'An inventor of an entity (such as an experimental procedure) for a research project.'
    }
    InvestigationRole_PostdoctoralResearcher = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/postdoctoral-researcher',
        'title': 'postdoctoral researcher',
        'description': 'A post-doctoral researcher involved in the research project.'
    }
    InvestigationRole_PrincipleInvestigator = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/principle-investigator',
        'title': 'principle investigator',
        'description': 'The principle investigator of the research project.'
    }
    InvestigationRole_ProjectStudent = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/project-student',
        'title': 'project-student',
        'description': 'A person engaged in the research project as part of studying for an undergraduate degree at a '
                       'university.'
    }
    InvestigationRole_ResearchAssistant = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/research-assistant',
        'title': 'research assistant',
        'description': 'A research assistant involved in the research project.'
    }
    InvestigationRole_ResearchStudent = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/research-student',
        'title': 'research student',
        'description': 'A person engaged in the research project as part of studying for an undergraduate degree at a '
                       'university or research institute.'
    }
    InvestigationRole_Researcher = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/researcher',
        'title': 'researcher',
        'description': 'A person involved in the research project.'
    }
    InvestigationRole_Scholar = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/scholar',
        'title': 'scholar',
        'description': 'An academic who undertakes scholarly activities as part of the research project.'
    }
    InvestigationRole_ServiceEngineer = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/service-engineer',
        'title': 'service-engineer',
        'description': 'A person who services, maintains and repairs equipment, facilities or technical infrastructure '
                       'used in the research project.'
    }
    InvestigationRole_Technician = {
        'class': 'http://purl.org/spar/scoro/InvestigationRole',
        'member': 'http://purl.org/spar/scoro/technician',
        'title': 'technician',
        'description': 'A person who provides technical assistance in some endeavour within a research project.'
    }
    OrganizationalRole_Administrator = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/administrator',
        'title': 'administrator',
        'description': 'A person who is responsible for the day to day management and running of the organisation.'
    }
    OrganizationalRole_Affiliate = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/affiliate',
        'title': 'affiliate',
        'description': 'An agent that is affiliated with the organisation in the context of an endeavour.'
    }
    OrganizationalRole_Agent = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/agent',
        'title': 'agent',
        'description': 'An agent that acts on behalf of another agent.'
    }
    OrganizationalRole_CEO = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/ceo',
        'title': 'CEO',
        'description': 'The person who is responsible for directing and managing the business of the organisation.'
    }
    OrganizationalRole_CTO = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/cto',
        'title': 'CTO',
        'description': 'The person who is responsible for directing and managing the technical development of the '
                       'organisation.'
    }
    OrganizationalRole_CollegeFellow = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/college-fellow',
        'title': 'college-fellow',
        'description': 'A person that has been made a fellow of a college'
    }
    OrganizationalRole_CollegeHead = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/college-head',
        'title': 'college-head',
        'description': 'A person that leads a college.'
    }
    OrganizationalRole_ContactPerson = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/contact-person',
        'title': 'contact person',
        'description': 'A person whom others should correspond with about the organisation, either generally or for '
                       'specific information/activities.'
    }
    OrganizationalRole_DepartmentalAdministrator = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/departmental-administrator',
        'title': 'departmental-administrator',
        'description': 'A person who is responsible for the day to day management and running of the department or '
                       'team within the organisation.'
    }
    OrganizationalRole_Director = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/director',
        'title': 'director',
        'description': 'A person that leads an activity or organisation.'
    }
    OrganizationalRole_Employee = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/employee',
        'title': 'employee',
        'description': 'A person who enters into a contract to undertake work on an agent\'s behalf in return for a '
                       'wage.'
    }
    OrganizationalRole_Employer = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/employer',
        'title': 'employer',
        'description': 'An agent that employees one or more people to undertake work on behalf of that agent.'
    }
    OrganizationalRole_HeadOfDepartment = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/head-of-department',
        'title': 'head-of-department',
        'description': 'The person that leads a team or department within the organisation.'
    }
    OrganizationalRole_HostInstitution = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/host-institution',
        'title': 'host-institution',
        'description': 'An agent that hosts another agent, endeavour or event.'
    }
    OrganizationalRole_Manager = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/manager',
        'title': 'manager',
        'description': 'A person who is responsible for managing the day to day activities of a team, department '
                       'within the organisation.'
    }
    OrganizationalRole_Member = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/Member',
        'title': 'Member',
        'description': 'An agent that belongs to a team, department or endeavour within the organisation.'
    }
    OrganizationalRole_NonAcademicStaffMember = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/non-academic-staff-member',
        'title': 'non-academic staff member',
        'description': 'A person employed within the organisation that is not an academic.'
    }
    OrganizationalRole_Organizer = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/organizer',
        'title': 'organizer',
        'description': 'An agent that arranges and runs an endeavour.'
    }
    OrganizationalRole_Participant = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/participant',
        'title': 'participant',
        'description': 'An agent that is involved in an endeavour.'
    }
    OrganizationalRole_Partner = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/partner',
        'title': 'partner',
        'description': 'An agent that partners with one or more people in the organisation as part of a shared '
                       'endeavour.'
    }
    OrganizationalRole_PatentHolder = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/patent-holder',
        'title': 'patent holder',
        'description': 'An agent that holds a patent.'
    }
    OrganizationalRole_Possessor = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/possessor',
        'title': 'possessor',
        'description': 'An agent that possesses a resource within the organisation.'
    }
    OrganizationalRole_ProgrammeManager = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/programme-manager',
        'title': 'programme manager',
        'description': 'A person who is responsible for managing a programme of activities within the organisation.'
    }
    OrganizationalRole_Registrar = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/registrar',
        'title': 'registrar',
        'description': 'An agent who has responsibility to keep official records within the organisation.'
    }
    OrganizationalRole_RegistrationAgency = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/registration-agency',
        'title': 'registration agency',
        'description': 'An agent with responsibility to register resources in a given domain.'
    }
    OrganizationalRole_RegistrationAuthority = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/registration-authority',
        'title': 'registration authority',
        'description': 'An agent with responsibility for managing the criteria to register resource in a given domain.'
    }
    OrganizationalRole_RightsHolder = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/rights-holder',
        'title': 'rights holder',
        'description': 'An agent that controls or owns the legal rights of a resource or outcomes of an endeavour.'
    }
    OrganizationalRole_Spokesperson = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/spokesperson',
        'title': 'spokesperson',
        'description': 'A person that makes statements on behalf of the organisation.'
    }
    OrganizationalRole_Stakeholder = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/stakeholder',
        'title': 'stakeholder',
        'description': 'An agent with an interest or concern in something.'
    }
    OrganizationalRole_Successor = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/successor',
        'title': 'successor',
        'description': 'The entity that succeeds another, such as a resource, agent or endeavour.'
    }
    OrganizationalRole_ViceChancellor = {
        'class': 'http://purl.com/spar/scoro/OrganizationRole',
        'member': 'http://purl/com/spar/scoro/vice-chancellor',
        'title': 'vice chancellor',
        'description': 'The person who is responsible for directing and managing the business and academic activities '
                       'of the university.'
    }
    ProjectRole_CoApplicant = {
        'class': 'http://purl.com/spar/scoro/ProjectRole',
        'member': 'http://purl/com/spar/scoro/co-applicant',
        'title': 'co-applicant',
        'description': 'A person who co-applies for the grant.'
    }
    ProjectRole_LeadApplicant = {
        'class': 'http://purl.com/spar/scoro/ProjectRole',
        'member': 'http://purl/com/spar/scoro/lead-applicant',
        'title': 'lead applicant',
        'description': 'The person who leads the application for the grant.'
    }
    ProjectRole_ProjectLeader = {
        'class': 'http://purl.com/spar/scoro/ProjectRole',
        'member': 'http://purl/com/spar/scoro/project-leader',
        'title': 'project leader',
        'description': 'The agent who leads a project.'
    }
    ProjectRole_ProjectManager = {
        'class': 'http://purl.com/spar/scoro/ProjectRole',
        'member': 'http://purl/com/spar/scoro/project-manager',
        'title': 'project manager',
        'description': 'A person who is responsible for managing the day to day activities of the project.'
    }
    ProjectRole_ProjectMember = {
        'class': 'http://purl.com/spar/scoro/ProjectRole',
        'member': 'http://purl/com/spar/scoro/',
        'title': 'project member',
        'description': 'An agent that belongs to the project.'
    }
    ProjectRole_WorkpackageLeader = {
        'class': 'http://purl.com/spar/scoro/ProjectRole',
        'member': 'http://purl/com/spar/scoro/workpackage-leader',
        'title': 'work package leader',
        'description': 'The agent that is responsible for the work within a work package or component of the project.'
    }


class Participant(db.Model):
    """
    Represents the relationship between an individual and a research project (i.e. their role)
    """
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    role = db.Column(db.Enum(ParticipantRole), nullable=True)

    project = db.relationship("Project", back_populates="participants")
    person = db.relationship("Person", back_populates="participation")

    def __repr__(self):
        return f"<Person:Project { self.neutral_id } ({ self.person.neutral_id }:{ self.project.neutral_id })>"

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
        participant_nid = '01D5T4N25RV2062NVVQKZ9NBYX'

        if not db.session.query(exists().where(Participant.neutral_id == participant_nid)).scalar():
            person_project = Participant(
                neutral_id=participant_nid,
                project=Project.query.filter_by(neutral_id='01D5M0CFQV4M7JASW7F87SRDYB').one(),
                person=Person.query.filter_by(neutral_id='01D5MHQN3ZPH47YVSVQEVB0DAE').one(),
                role=ParticipantRole.InvestigationRole_PrincipleInvestigator
            )
            db.session.add(person_project)

        if quantity > 1:
            pass
