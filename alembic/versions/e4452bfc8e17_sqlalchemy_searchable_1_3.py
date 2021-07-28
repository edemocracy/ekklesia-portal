"""sqlalchemy-searchable 1.3

Revision ID: e4452bfc8e17
Revises: 4c6df443cb98
Create Date: 2021-07-28 00:16:53.014716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4452bfc8e17'
down_revision = '4c6df443cb98'
branch_labels = None
depends_on = None


functions_sql = """
CREATE OR REPLACE FUNCTION parse_websearch(config regconfig, search_query text)
RETURNS tsquery AS $$
SELECT
    string_agg(
        (
            CASE
                WHEN position('''' IN words.word) > 0 THEN CONCAT(words.word, ':*')
                ELSE words.word
            END
        ),
        ' '
    )::tsquery
FROM (
    SELECT trim(
        regexp_split_to_table(
            websearch_to_tsquery(config, lower(search_query))::text,
            ' '
        )
    ) AS word
) AS words
$$ LANGUAGE SQL IMMUTABLE;


CREATE OR REPLACE FUNCTION parse_websearch(search_query text)
RETURNS tsquery AS $$
SELECT parse_websearch('pg_catalog.simple', search_query);
$$ LANGUAGE SQL IMMUTABLE;
"""


def upgrade():
    op.execute(functions_sql)


def downgrade():
    op.execute("DROP FUNCTION parse_websearch(config regconfig, search_query text)")
    op.execute("DROP FUNCTION parse_websearch(search_query text)")
