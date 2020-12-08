"""Empty default for proposition.external_fields

Revision ID: 6d782ad96592
Revises: 0b17ab7f0a04
Create Date: 2020-08-15 23:33:04.586549

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6d782ad96592'
down_revision = '0b17ab7f0a04'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE propositions SET external_fields = '{}' WHERE external_fields IS NULL")
    op.alter_column('propositions', 'external_fields',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               server_default='{}',
               existing_comment='Fields that are imported from or exported to other systems but are not interpreted by the portal.',
               nullable=False)


def downgrade():
    op.alter_column('propositions', 'external_fields',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               server_default=None,
               existing_comment='Fields that are imported from or exported to other systems but are not interpreted by the portal.',
               nullable=True)
