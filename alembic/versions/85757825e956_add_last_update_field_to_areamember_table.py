"""Add last_update field to AreaMember table

Revision ID: 85757825e956
Revises: e4452bfc8e17
Create Date: 2023-07-13 22:43:09.427028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85757825e956'
down_revision = 'e4452bfc8e17'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('areamembers', sa.Column('last_update', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='last membership update'))


def downgrade():
    op.drop_column('areamembers', 'last_update')
