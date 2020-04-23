"""Add datetime suffix _at to Proposition.submitted and qualified

Revision ID: 88f61bc7227e
Revises:
Create Date: 2020-04-23 18:35:30.235844

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '88f61bc7227e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('propositions', 'submitted', new_column_name='submitted_at')
    op.alter_column('propositions', 'qualified', new_column_name='qualified_at')


def downgrade():
    op.alter_column('propositions', 'submitted_at', new_column_name='submitted')
    op.alter_column('propositions', 'qualified_at', new_column_name='qualified')
