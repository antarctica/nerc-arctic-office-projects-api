"""Adding Person and Participant entities

Revision ID: 631f964e665f
Revises: d919f20fe946
Create Date: 2019-03-10 19:33:37.135571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631f964e665f'
down_revision = 'd919f20fe946'
branch_labels = None
depends_on = None


def upgrade():
    # Person
    #
    op.create_table('people',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.Column('orcid_id', sa.String(length=64), nullable=True),
        sa.Column('logo_url', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('orcid_id')
    )
    op.create_index(op.f('ix_people_neutral_id'), 'people', ['neutral_id'], unique=True)

    # Participant
    #
    op.create_table('participants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('neutral_id', sa.String(length=32), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('AuthorshipRole_ArticleGuarantor', 'AuthorshipRole_Author',
                                  'AuthorshipRole_ConsortiumAuthor', 'AuthorshipRole_CorrespondingAuthor',
                                  'AuthorshipRole_Illustrator', 'AuthorshipRole_Photographer',
                                  'AuthorshipRole_PrincipalAuthor', 'AuthorshipRole_SeniorAuthor',
                                  'DataRole_AccessProvider', 'DataRole_Curator', 'DataRole_DataCreator',
                                  'DataRole_DataCurator', 'DataRole_DataManager', 'DataRole_DataPublisher',
                                  'DataRole_DataUser', 'DataRole_EmbargoController',
                                  'DataRole_RepositoryManager',
                                  'DataRole_WebMaster', 'FinancialRole_Accountant', 'FinancialRole_Auditor',
                                  'FinancialRole_Claimant', 'FinancialRole_Contractor',
                                  'FinancialRole_FinancialController', 'FinancialRole_Funder',
                                  'FinancialRole_FundingRecipient', 'FinancialRole_Owner',
                                  'FinancialRole_Purchaser',
                                  'FinancialRole_Sponsor', 'FinancialRole_SubContractor',
                                  'FinancialRole_Supplier',
                                  'InvestigationRole_ChiefScientist', 'InvestigationRole_CoInvestigator',
                                  'InvestigationRole_Collaborator', 'InvestigationRole_ComputerProgrammer',
                                  'InvestigationRole_Consultant', 'InvestigationRole_Inventor',
                                  'InvestigationRole_PostdoctoralResearcher',
                                  'InvestigationRole_PrincipleInvestigator',
                                  'InvestigationRole_ProjectStudent', 'InvestigationRole_ResearchAssistant',
                                  'InvestigationRole_ResearchStudent', 'InvestigationRole_Researcher',
                                  'InvestigationRole_Scholar', 'InvestigationRole_ServiceEngineer',
                                  'InvestigationRole_Technician', 'OrganizationalRole_Administrator',
                                  'OrganizationalRole_Affiliate', 'OrganizationalRole_Agent',
                                  'OrganizationalRole_CEO', 'OrganizationalRole_CTO',
                                  'OrganizationalRole_CollegeFellow', 'OrganizationalRole_CollegeHead',
                                  'OrganizationalRole_ContactPerson',
                                  'OrganizationalRole_DepartmentalAdministrator',
                                  'OrganizationalRole_Director', 'OrganizationalRole_Employee',
                                  'OrganizationalRole_Employer', 'OrganizationalRole_HeadOfDepartment',
                                  'OrganizationalRole_HostInstitution', 'OrganizationalRole_Manager',
                                  'OrganizationalRole_Member', 'OrganizationalRole_NonAcademicStaffMember',
                                  'OrganizationalRole_Organizer', 'OrganizationalRole_Participant',
                                  'OrganizationalRole_Partner', 'OrganizationalRole_PatentHolder',
                                  'OrganizationalRole_Possessor', 'OrganizationalRole_ProgrammeManager',
                                  'OrganizationalRole_Registrar', 'OrganizationalRole_RegistrationAgency',
                                  'OrganizationalRole_RegistrationAuthority',
                                  'OrganizationalRole_RightsHolder',
                                  'OrganizationalRole_Spokesperson', 'OrganizationalRole_Stakeholder',
                                  'OrganizationalRole_Successor', 'OrganizationalRole_ViceChancellor',
                                  'ProjectRole_CoApplicant', 'ProjectRole_LeadApplicant',
                                  'ProjectRole_ProjectLeader',
                                  'ProjectRole_ProjectManager', 'ProjectRole_ProjectMember',
                                  'ProjectRole_WorkpackageLeader', name='participant_role'), nullable=True),
        sa.ForeignKeyConstraint(('person_id',), ['people.id'], ),
        sa.ForeignKeyConstraint(('project_id',), ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_participants_neutral_id'), 'participants', ['neutral_id'], unique=True)


def downgrade():
    # Participant
    #
    op.drop_index(op.f('ix_participants_neutral_id'), table_name='participants')
    op.drop_table('participants')
    sa.Enum(name='participant_role').drop(op.get_bind(), checkfirst=False)

    # Person
    #
    op.drop_index(op.f('ix_people_neutral_id'), table_name='people')
    op.drop_table('people')
