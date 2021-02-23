"""Add VotingPhaseType.description

Revision ID: 9801fcc513e6
Revises: e2ce064655e8
Create Date: 2021-02-23 17:44:48.507935

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9801fcc513e6'
down_revision = 'e2ce064655e8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('voting_phase_types', sa.Column('description', sa.Text(), server_default='', nullable=True))


def downgrade():
    op.drop_column('voting_phase_types', 'description')
