"""Add document and changeset tables

Revision ID: e9da2a1d0a47
Revises: 88f61bc7227e
Create Date: 2020-04-23 21:30:35.128509

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e9da2a1d0a47'
down_revision = '88f61bc7227e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'document', sa.Column('id', sa.Integer(), nullable=False), sa.Column('name', sa.String(), nullable=True),
        sa.Column('lang', sa.String(length=16), nullable=True), sa.Column('area_id', sa.Integer(), nullable=True),
        sa.Column('text', sa.Text(), nullable=True), sa.Column('description', sa.Text(), nullable=True),
        sa.Column('proposition_type_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['area_id'],
            ['subjectareas.id'],
        ), sa.ForeignKeyConstraint(
            ['proposition_type_id'],
            ['propositiontypes.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'lang', 'area_id', name='uq_document_name_lang_area_id'))
    op.create_table(
        'changeset', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('proposition_id', sa.Integer(), nullable=False),
        sa.Column(
            'section',
            sa.String(),
            nullable=True,
            comment='Identifier for the section of the document that is changed.'),
        sa.ForeignKeyConstraint(
            ['document_id'],
            ['document.id'],
        ), sa.ForeignKeyConstraint(
            ['proposition_id'],
            ['propositions.id'],
        ), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('changeset')
    op.drop_table('document')
