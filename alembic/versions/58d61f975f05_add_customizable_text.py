"""Add customizable_text

Revision ID: 58d61f975f05
Revises: 45e46ee4911f
Create Date: 2020-04-27 22:13:48.837415

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '58d61f975f05'
down_revision = '45e46ee4911f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customizable_text', sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('lang', sa.String(length=16), nullable=False), sa.Column('text', sa.Text(), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True), sa.PrimaryKeyConstraint('name', 'lang'))


def downgrade():
    op.drop_table('customizable_text')
