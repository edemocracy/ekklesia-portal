"""Add Proposition.author

Revision ID: fce689b4e91f
Revises: 2ef4af95efe9
Create Date: 2020-08-15 21:02:09.176120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fce689b4e91f'
down_revision = '2ef4af95efe9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('propositions', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_propositions_author_id_users'), 'propositions', 'users', ['author_id'], ['id'])


def downgrade():
    op.drop_constraint(op.f('fk_propositions_author_id_users'), 'propositions', type_='foreignkey')
    op.drop_column('propositions', 'author_id')
