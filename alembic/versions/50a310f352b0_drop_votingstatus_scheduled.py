"""Drop VotingStatus.SCHEDULED

Revision ID: 50a310f352b0
Revises: 9801fcc513e6
Create Date: 2021-07-06 20:33:29.509764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50a310f352b0'
down_revision = '9801fcc513e6'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("state_valid", "votingphases", "check")
    op.execute("ALTER TABLE votingphases ALTER COLUMN status DROP DEFAULT")
    op.execute("UPDATE votingphases SET status = 'PREPARING' WHERE status = 'SCHEDULED'")
    op.execute("ALTER TYPE votingstatus RENAME TO votingstatus_old")
    op.execute("CREATE TYPE votingstatus AS ENUM('PREPARING', 'VOTING', 'FINISHED', 'ABORTED')")
    op.execute((
        "ALTER TABLE votingphases ALTER COLUMN status TYPE votingstatus USING " +
        "status::text::votingstatus"
    ))
    op.execute("ALTER TABLE votingphases ALTER COLUMN status SET DEFAULT 'PREPARING'::votingstatus")
    op.execute("DROP TYPE votingstatus_old")
    op.create_check_constraint('state_valid',
        "votingphases",
        "status='PREPARING' OR (status!='PREPARING' AND target IS NOT NULL)")


def downgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE votingstatus ADD VALUE 'SCHEDULED'")
    op.execute("UPDATE votingphases SET status = 'SCHEDULED' WHERE status = 'PREPARING' AND target IS NOT NULL")
    op.drop_constraint("state_valid", "votingphases", "check")
    op.create_check_constraint('state_valid',
        "votingphases",
        "(status='PREPARING' AND target IS NULL) OR (status!='PREPARING' AND target IS NOT NULL)")
