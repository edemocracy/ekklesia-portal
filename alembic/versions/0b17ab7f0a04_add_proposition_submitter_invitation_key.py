"""Add Proposition.submitter_invitation_key

Revision ID: 0b17ab7f0a04
Revises: fce689b4e91f
Create Date: 2020-08-15 21:39:25.068276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b17ab7f0a04'
down_revision = 'fce689b4e91f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('propositions', sa.Column('submitter_invitation_key', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('propositions', 'submitter_invitation_key')
