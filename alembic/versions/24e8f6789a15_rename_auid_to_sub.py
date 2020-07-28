"""Rename auid to sub

Revision ID: 24e8f6789a15
Revises: a4817cb50cc4
Create Date: 2020-07-28 21:50:40.744548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24e8f6789a15'
down_revision = 'a4817cb50cc4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('userprofiles', 'auid', new_column_name='sub')


def downgrade():
    op.alter_column('userprofiles', 'sub', new_column_name='auid')
