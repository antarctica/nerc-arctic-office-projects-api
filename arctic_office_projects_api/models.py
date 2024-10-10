from enum import Enum

# noinspection PyPackageRequirements
from sqlalchemy.dialects import postgresql

# noinspection PyPackageRequirements
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import LtreeType, Ltree

from arctic_office_projects_api.extensions import db
from arctic_office_projects_api.utils import generate_countries_enum

ProjectCountry = generate_countries_enum(name="ProjectCountries")


class ParticipantRole(Enum):
    """
    Represents the members of the various role classes in the Scholarly Contributions and Roles Ontology (SCoRO)
    """

    AuthorshipRole_ArticleGuarantor = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/article-guarantor",
        "title": "article guarantor",
        "description": "A person who takes responsibility for the integrity of the article as a whole, from the "
        "inception of the research investigation to the published research article.",
    }
    AuthorshipRole_Author = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/pro/author",
        "title": "author",
        "description": "A person who has authorship of the work.",
    }
    AuthorshipRole_ConsortiumAuthor = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/consortium-author",
        "title": "consortium author",
        "description": "An organisation or consortium that has contributed collectively to the work and is named in "
        "the list of authors.",
    }
    AuthorshipRole_CorrespondingAuthor = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/corresponding-author",
        "title": "corresponding author",
        "description": "An author of the work with whom editors and readers should correspond concerning it.",
    }
    AuthorshipRole_Illustrator = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/illustrator",
        "title": "illustrator",
        "description": "A illustrator of, or for, the work.",
    }
    AuthorshipRole_Photographer = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/photographer",
        "title": "photographer",
        "description": "A photographer of, or for, the work.",
    }
    AuthorshipRole_PrincipalAuthor = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/principal-author",
        "title": "principal author",
        "description": "An author of the work considered to have contributed most.",
    }
    AuthorshipRole_SeniorAuthor = {
        "class": "http://purl.org/spar/scoro/AuthorshipRole",
        "member": "http://purl.org/spar/scoro/senior-author",
        "title": "senior author",
        "description": "A senior author of the work.",
    }
    DataRole_AccessProvider = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/access-provider",
        "title": "access provider",
        "description": "An agent who provides access to a resource.",
    }
    DataRole_Curator = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/curator",
        "title": "curator",
        "description": "An agent who documents, cares for and manages collections of resources.",
    }
    DataRole_DataCreator = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/data-creator",
        "title": "data creator",
        "description": "A person who creates, originates, gathers or collects new data.",
    }
    DataRole_DataCurator = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/data-curator",
        "title": "data curator",
        "description": "A person who is responsible for reviewing, enhancing, cleaning, or standardizing data and "
        "their associated metadata for their long-term preservation.",
    }
    DataRole_DataManager = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/data-manager",
        "title": "data manager",
        "description": "A person who is responsible for day-to-day management, maintenance and back-up of data.",
    }
    DataRole_DataPublisher = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/data-publisher",
        "title": "data publisher",
        "description": "An agent who publishes data.",
    }
    DataRole_DataUser = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/data-user",
        "title": "data user",
        "description": "A person who uses or re-uses existing data.",
    }
    DataRole_EmbargoController = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/embargo-controller",
        "title": "embargo controller",
        "description": "A person who has responsibility for setting and lifting embargos that restrict access to a "
        "dataset (or other resource) for a specified period of time.",
    }
    DataRole_RepositoryManager = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/repository-manager",
        "title": "repository manager",
        "description": "A person who managers a repository where resources are given secure long-term storage.",
    }
    DataRole_WebMaster = {
        "class": "http://purl.org/spar/scoro/DataRole",
        "member": "http://purl.org/spar/scoro/web-master",
        "title": "web master",
        "description": "A person who has responsibility for maintaining a web site and its content.",
    }
    FinancialRole_Accountant = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/accountant ",
        "title": "accountant ",
        "description": "A person who has responsibility for managing financial accounts.",
    }
    FinancialRole_Auditor = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/auditor",
        "title": "auditor",
        "description": "A person who has responsibility for conducting formal audits of financial accounts.",
    }
    FinancialRole_Claimant = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/claimant",
        "title": "claimant",
        "description": "A person making a financial claim, such as for expenses.",
    }
    FinancialRole_Contractor = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/",
        "title": "Contractor",
        "description": "An agent who enters into a contract to undertake specified work or to supply specified "
        "services in return for payment.",
    }
    FinancialRole_FinancialController = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/financial-controller",
        "title": "financial controller",
        "description": "An agent with responsibility for controlling a budget, including authorising expenditure.",
    }
    FinancialRole_Funder = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/funder",
        "title": "funder",
        "description": "An agent that provides funds, such as for a research project.",
    }
    FinancialRole_FundingRecipient = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/funding-recipient",
        "title": "funding recipient",
        "description": "An agent who is the official recipient of funding, for example the university at which the "
        "funded research project leader is a member.",
    }
    FinancialRole_Owner = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/owner",
        "title": "owner",
        "description": "An agent that owns something with actual or potential financial value.",
    }
    FinancialRole_Purchaser = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/purchaser",
        "title": "purchaser",
        "description": "An agent with responsibility for making purchases of goods or services from a budget.",
    }
    FinancialRole_Sponsor = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/sponsor",
        "title": "sponsor",
        "description": "An agent that provides funds or support to an agent or endeavour, often in return for access "
        "to the exploitable commercial potential, or endeavour's output.",
    }
    FinancialRole_SubContractor = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/sub-contractor",
        "title": "sub-contractor",
        "description": "An agent who enters into a contract to take over part of another contractor's obligation.",
    }
    FinancialRole_Supplier = {
        "class": "http://purl.org/spar/scoro/FinancialRole",
        "member": "http://purl.org/spar/scoro/supplier",
        "title": "supplier",
        "description": "An agent with responsibility to provide goods or services in exchange for payment.",
    }
    InvestigationRole_ChiefScientist = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/chief-scientist",
        "title": "chief scientist",
        "description": "The scientist who leads a research group or organization.",
    }
    InvestigationRole_CoInvestigator = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/co-investigator",
        "title": "co-investigator",
        "description": "A co-investigator of the research project.",
    }
    InvestigationRole_Collaborator = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/collaborator",
        "title": "Collaborator",
        "description": "A person, typically from another group or institution, who collaborates with those undertaking "
        "a research project.",
    }
    InvestigationRole_ComputerProgrammer = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/computer-programmer",
        "title": "computer programmer",
        "description": "A person who develops computer software for a research project",
    }
    InvestigationRole_Consultant = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/consultant",
        "title": "consultant",
        "description": "A person who provides expertise or services for a research project",
    }
    InvestigationRole_Inventor = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/inventor",
        "title": "inventor",
        "description": "An inventor of an entity (such as an experimental procedure) for a research project.",
    }
    InvestigationRole_PostdoctoralResearcher = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/postdoctoral-researcher",
        "title": "postdoctoral researcher",
        "description": "A post-doctoral researcher involved in the research project.",
    }
    InvestigationRole_PrincipleInvestigator = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/principle-investigator",
        "title": "principle investigator",
        "description": "The principle investigator of the research project.",
    }
    InvestigationRole_ProjectStudent = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/project-student",
        "title": "project-student",
        "description": "A person engaged in the research project as part of studying for an undergraduate degree at a "
        "university.",
    }
    InvestigationRole_ResearchAssistant = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/research-assistant",
        "title": "research assistant",
        "description": "A research assistant involved in the research project.",
    }
    InvestigationRole_ResearchStudent = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/research-student",
        "title": "research student",
        "description": "A person engaged in the research project as part of studying for an undergraduate degree at a "
        "university or research institute.",
    }
    InvestigationRole_Researcher = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/researcher",
        "title": "researcher",
        "description": "A person involved in the research project.",
    }
    InvestigationRole_Scholar = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/scholar",
        "title": "scholar",
        "description": "An academic who undertakes scholarly activities as part of the research project.",
    }
    InvestigationRole_ServiceEngineer = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/service-engineer",
        "title": "service-engineer",
        "description": "A person who services, maintains and repairs equipment, facilities or technical infrastructure "
        "used in the research project.",
    }
    InvestigationRole_Technician = {
        "class": "http://purl.org/spar/scoro/InvestigationRole",
        "member": "http://purl.org/spar/scoro/technician",
        "title": "technician",
        "description": "A person who provides technical assistance in some endeavour within a research project.",
    }
    OrganizationalRole_Administrator = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/administrator",
        "title": "administrator",
        "description": "A person who is responsible for the day to day management and running of the organisation.",
    }
    OrganizationalRole_Affiliate = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/affiliate",
        "title": "affiliate",
        "description": "An agent that is affiliated with the organisation in the context of an endeavour.",
    }
    OrganizationalRole_Agent = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/agent",
        "title": "agent",
        "description": "An agent that acts on behalf of another agent.",
    }
    OrganizationalRole_CEO = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/ceo",
        "title": "CEO",
        "description": "The person who is responsible for directing and managing the business of the organisation.",
    }
    OrganizationalRole_CTO = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/cto",
        "title": "CTO",
        "description": "The person who is responsible for directing and managing the technical development of the "
        "organisation.",
    }
    OrganizationalRole_CollegeFellow = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/college-fellow",
        "title": "college-fellow",
        "description": "A person that has been made a fellow of a college",
    }
    OrganizationalRole_CollegeHead = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/college-head",
        "title": "college-head",
        "description": "A person that leads a college.",
    }
    OrganizationalRole_ContactPerson = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/contact-person",
        "title": "contact person",
        "description": "A person whom others should correspond with about the organisation, either generally or for "
        "specific information/activities.",
    }
    OrganizationalRole_DepartmentalAdministrator = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/departmental-administrator",
        "title": "departmental-administrator",
        "description": "A person who is responsible for the day to day management and running of the department or "
        "team within the organisation.",
    }
    OrganizationalRole_Director = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/director",
        "title": "director",
        "description": "A person that leads an activity or organisation.",
    }
    OrganizationalRole_Employee = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/employee",
        "title": "employee",
        "description": "A person who enters into a contract to undertake work on an agent's behalf in return for a "
        "wage.",
    }
    OrganizationalRole_Employer = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/employer",
        "title": "employer",
        "description": "An agent that employees one or more people to undertake work on behalf of that agent.",
    }
    OrganizationalRole_HeadOfDepartment = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/head-of-department",
        "title": "head-of-department",
        "description": "The person that leads a team or department within the organisation.",
    }
    OrganizationalRole_HostInstitution = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/host-institution",
        "title": "host-institution",
        "description": "An agent that hosts another agent, endeavour or event.",
    }
    OrganizationalRole_Manager = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/manager",
        "title": "manager",
        "description": "A person who is responsible for managing the day to day activities of a team, department "
        "within the organisation.",
    }
    OrganizationalRole_Member = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/Member",
        "title": "Member",
        "description": "An agent that belongs to a team, department or endeavour within the organisation.",
    }
    OrganizationalRole_NonAcademicStaffMember = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/non-academic-staff-member",
        "title": "non-academic staff member",
        "description": "A person employed within the organisation that is not an academic.",
    }
    OrganizationalRole_Organizer = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/organizer",
        "title": "organizer",
        "description": "An agent that arranges and runs an endeavour.",
    }
    OrganizationalRole_Participant = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/participant",
        "title": "participant",
        "description": "An agent that is involved in an endeavour.",
    }
    OrganizationalRole_Partner = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/partner",
        "title": "partner",
        "description": "An agent that partners with one or more people in the organisation as part of a shared "
        "endeavour.",
    }
    OrganizationalRole_PatentHolder = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/patent-holder",
        "title": "patent holder",
        "description": "An agent that holds a patent.",
    }
    OrganizationalRole_Possessor = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/possessor",
        "title": "possessor",
        "description": "An agent that possesses a resource within the organisation.",
    }
    OrganizationalRole_ProgrammeManager = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/programme-manager",
        "title": "programme manager",
        "description": "A person who is responsible for managing a programme of activities within the organisation.",
    }
    OrganizationalRole_Registrar = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/registrar",
        "title": "registrar",
        "description": "An agent who has responsibility to keep official records within the organisation.",
    }
    OrganizationalRole_RegistrationAgency = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/registration-agency",
        "title": "registration agency",
        "description": "An agent with responsibility to register resources in a given domain.",
    }
    OrganizationalRole_RegistrationAuthority = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/registration-authority",
        "title": "registration authority",
        "description": "An agent with responsibility for managing the criteria to register resource in a given domain.",
    }
    OrganizationalRole_RightsHolder = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/rights-holder",
        "title": "rights holder",
        "description": "An agent that controls or owns the legal rights of a resource or outcomes of an endeavour.",
    }
    OrganizationalRole_Spokesperson = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/spokesperson",
        "title": "spokesperson",
        "description": "A person that makes statements on behalf of the organisation.",
    }
    OrganizationalRole_Stakeholder = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/stakeholder",
        "title": "stakeholder",
        "description": "An agent with an interest or concern in something.",
    }
    OrganizationalRole_Successor = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/successor",
        "title": "successor",
        "description": "The entity that succeeds another, such as a resource, agent or endeavour.",
    }
    OrganizationalRole_ViceChancellor = {
        "class": "http://purl.com/spar/scoro/OrganizationRole",
        "member": "http://purl/com/spar/scoro/vice-chancellor",
        "title": "vice chancellor",
        "description": "The person who is responsible for directing and managing the business and academic activities "
        "of the university.",
    }
    ProjectRole_CoApplicant = {
        "class": "http://purl.com/spar/scoro/ProjectRole",
        "member": "http://purl/com/spar/scoro/co-applicant",
        "title": "co-applicant",
        "description": "A person who co-applies for the grant.",
    }
    ProjectRole_LeadApplicant = {
        "class": "http://purl.com/spar/scoro/ProjectRole",
        "member": "http://purl/com/spar/scoro/lead-applicant",
        "title": "lead applicant",
        "description": "The person who leads the application for the grant.",
    }
    ProjectRole_ProjectLeader = {
        "class": "http://purl.com/spar/scoro/ProjectRole",
        "member": "http://purl/com/spar/scoro/project-leader",
        "title": "project leader",
        "description": "The agent who leads a project.",
    }
    ProjectRole_ProjectManager = {
        "class": "http://purl.com/spar/scoro/ProjectRole",
        "member": "http://purl/com/spar/scoro/project-manager",
        "title": "project manager",
        "description": "A person who is responsible for managing the day to day activities of the project.",
    }
    ProjectRole_ProjectMember = {
        "class": "http://purl.com/spar/scoro/ProjectRole",
        "member": "http://purl/com/spar/scoro/",
        "title": "project member",
        "description": "An agent that belongs to the project.",
    }
    ProjectRole_WorkpackageLeader = {
        "class": "http://purl.com/spar/scoro/ProjectRole",
        "member": "http://purl/com/spar/scoro/workpackage-leader",
        "title": "work package leader",
        "description": "The agent that is responsible for the work within a work package or component of the project.",
    }


class GrantStatus(Enum):
    """
    Represents the various states of a research grant
    """

    Accepted = "accepted"
    Active = "active"
    Approved = "approved"
    Authorised = "authorised"
    Closed = "closed"
    Completed = "completed"
    Terminated = "terminated"
    Pending = "pending"
    Unknown = "unknown"


class GrantCurrency(Enum):
    """
    Represents the various currencies of a research grant
    """

    GBP = {"iso_4217_code": "GBP", "major_symbol": "£"}
    EUR = {"iso_4217_code": "EUR", "major_symbol": "€"}
    NOK = {"iso_4217_code": "NOK", "major_symbol": "kr"}
    CAD = {"iso_4217_code": "CAD", "major_symbol": "$"}


class Project(db.Model):
    """
    Represents information about a research project
    """

    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    grant_reference = db.Column(db.Text(), nullable=False)
    title = db.Column(db.Text(), nullable=False)
    acronym = db.Column(db.Text(), nullable=True)
    abstract = db.Column(db.Text(), nullable=True)
    website = db.Column(db.Text(), nullable=True)
    publications = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    access_duration = db.Column(postgresql.DATERANGE(), nullable=False)
    project_duration = db.Column(postgresql.DATERANGE(), nullable=False)
    country = db.Column(db.Enum(ProjectCountry), nullable=True)
    lead_project = db.Column(db.Boolean(), nullable=True)
    participants = db.relationship("Participant", back_populates="project")
    allocations = db.relationship("Allocation", back_populates="project")
    categorisations = db.relationship("Categorisation", back_populates="project")

    def __repr__(self):
        return f"<Project { self.neutral_id }>"  # pragma: no cover


class Person(db.Model):
    """
    Represents information about an individual involved in research projects
    """

    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(
        db.Integer, db.ForeignKey("organisations.id"), nullable=True
    )
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    first_name = db.Column(db.Text(), nullable=True)
    last_name = db.Column(db.Text(), nullable=True)
    orcid_id = db.Column(db.String(64), unique=True, nullable=True)
    logo_url = db.Column(db.Text(), nullable=True)

    organisation = db.relationship("Organisation", back_populates="people")
    participation = db.relationship("Participant", back_populates="person")

    def __repr__(self):
        return f"<Person { self.neutral_id } ({ self.last_name }, { self.first_name })>"  # pragma: no cover


class Participant(db.Model):
    """
    Represents the relationship between an individual and a research project (i.e. their role)
    """

    __tablename__ = "participants"
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    role = db.Column(db.Enum(ParticipantRole), nullable=True)

    project = db.relationship("Project", back_populates="participants")
    person = db.relationship("Person", back_populates="participation")

    def __repr__(self):
        return f"<Participant { self.neutral_id } ({ self.person.neutral_id }:{ self.project.neutral_id })>"  # pragma: no cover


class Grant(db.Model):
    """
    Represents information about a research grant
    """

    __tablename__ = "grants"
    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(
        db.Integer, db.ForeignKey("organisations.id"), nullable=True
    )
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    reference = db.Column(db.Text(), unique=True, nullable=False)
    title = db.Column(db.Text(), nullable=False)
    abstract = db.Column(db.Text(), nullable=True)
    website = db.Column(db.Text(), nullable=True)
    publications = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    duration = db.Column(postgresql.DATERANGE(), nullable=False)
    status = db.Column(db.Enum(GrantStatus), nullable=False)
    total_funds = db.Column(db.Numeric(24, 2), nullable=True)
    total_funds_currency = db.Column(db.Enum(GrantCurrency), nullable=True)
    lead_project = db.Column(db.Boolean(), nullable=True)
    funder = db.relationship("Organisation", back_populates="grants")
    allocations = db.relationship("Allocation", back_populates="grant")

    def __repr__(self):
        return f"<Grant { self.neutral_id } ({ self.reference })>"  # pragma: no cover


class Allocation(db.Model):
    """
    Represents the relationship between an research grant and a research project (i.e. the funding for a project)
    """

    __tablename__ = "allocations"
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    grant_id = db.Column(db.Integer, db.ForeignKey("grants.id"), nullable=False)

    project = db.relationship("Project", back_populates="allocations")
    grant = db.relationship("Grant", back_populates="allocations")

    def __repr__(self):
        return f"<Allocation { self.neutral_id } ({ self.grant.neutral_id }:{ self.project.neutral_id })>"  # pragma: no cover


class Organisation(db.Model):
    """
    Represents an organisation, either as an agent (e.g. a funder) or an entity (e.g. that an individual belongs to)
    """

    __tablename__ = "organisations"
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    grid_identifier = db.Column(db.Text(), nullable=True)
    ror_identifier = db.Column(db.Text(), nullable=True)
    name = db.Column(db.Text(), nullable=False)
    acronym = db.Column(db.Text(), nullable=True)
    website = db.Column(db.Text(), nullable=True)
    logo_url = db.Column(db.Text(), nullable=True)

    grants = db.relationship("Grant", back_populates="funder")
    people = db.relationship("Person", back_populates="organisation")

    def __repr__(self):
        return f"<Organisation { self.neutral_id } ({ self.name })>"  # pragma: no cover


class CategoryScheme(db.Model):
    """
    Represents a category scheme, an entity that defines and contains a series of category terms
    """

    __tablename__ = "category_schemes"
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    name = db.Column(db.Text(), nullable=False)
    acronym = db.Column(db.Text(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    version = db.Column(db.Text(), nullable=True)
    revision = db.Column(db.Text(), nullable=True)
    namespace = db.Column(db.Text(), nullable=False)
    root_concepts = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=False
    )

    category_terms = db.relationship("CategoryTerm", back_populates="category_scheme")

    def __repr__(self):
        return (
            f"<CategoryScheme { self.neutral_id } ({ self.name })>"  # pragma: no cover
        )


class CategoryTerm(db.Model):
    """
    Represents a category term, an entity that defines a single concept with a category scheme
    """

    __tablename__ = "category_terms"
    id = db.Column(db.Integer, primary_key=True)
    category_scheme_id = db.Column(
        db.Integer, db.ForeignKey("category_schemes.id"), nullable=False
    )
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    scheme_identifier = db.Column(db.Text(), nullable=False)
    scheme_notation = db.Column(db.Text(), nullable=True)
    name = db.Column(db.Text(), nullable=False)
    aliases = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    definitions = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    examples = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    notes = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    scope_notes = db.Column(
        postgresql.ARRAY(db.Text(), dimensions=1, zero_indexes=True), nullable=True
    )
    path = db.Column(LtreeType, nullable=False, index=True)

    category_scheme = db.relationship("CategoryScheme", back_populates="category_terms")
    categorisations = db.relationship("Categorisation", back_populates="category_term")

    @hybrid_property
    def parent_category_term(self):
        """
        Hybrid property representing the parent (CategoryTerm) of a CategoryTerm, if one exists

        Performs a query based on the CategoryTerm.path Ltree property. If the path of the CategoryTerm is a single
        (root) level (e.g. 'root' rather than 'root.foo.bar') then there isn't a parent CategoryTerm and this property
        is made empty.

        Otherwise the current path is shortened (up) by a single level and used to find the relevant parent
        CategoryTerm (i.e. '1.2.3' becomes '1.2').

        :rtype CategoryTerm
        :return: CategoryTerm that is a parent of the current CategoryTerm as determined by the Ltree column
        """
        parent_category_term_path = Ltree(self.path)
        if len(parent_category_term_path) == 1:
            return None

        parent_category_term_path = Ltree(self.path)[:-1]

        return CategoryTerm.query.filter_by(path=parent_category_term_path).first()

    def __repr__(self):
        return f"<CategoryTerm { self.neutral_id } ({ self.category_scheme.name } - '{ self.name }')>"  # pragma: no cover


class Categorisation(db.Model):
    """
    Represents the relationship between a category term and a project (i.e. the categories of a project)
    """

    __tablename__ = "categorisations"
    id = db.Column(db.Integer, primary_key=True)
    neutral_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    category_term_id = db.Column(
        db.Integer, db.ForeignKey("category_terms.id"), nullable=False
    )

    project = db.relationship("Project", back_populates="categorisations")
    category_term = db.relationship("CategoryTerm", back_populates="categorisations")

    def __repr__(self):
        return f"<Categorisation { self.neutral_id } ({ self.category_term.neutral_id }:{ self.project.neutral_id })>"  # pragma: no cover
