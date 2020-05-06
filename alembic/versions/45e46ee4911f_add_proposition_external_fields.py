"""Add Proposition.external_fields

Revision ID: 45e46ee4911f
Revises: e9da2a1d0a47
Create Date: 2020-04-23 21:31:51.589489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '45e46ee4911f'
down_revision = 'e9da2a1d0a47'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'propositions',
        sa.Column(
            'external_fields',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment='Fields that are imported from or exported to other systems but are not interpreted by the portal.')
    )


def downgrade():
    op.drop_column('propositions', 'external_fields')
