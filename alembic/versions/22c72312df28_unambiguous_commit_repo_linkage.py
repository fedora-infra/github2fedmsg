"""Link repos and commits unambiguously.

Revision ID: 22c72312df28
Revises: 25ecbd961535
Create Date: 2013-03-26 14:58:53.691182

"""

# revision identifiers, used by Alembic.
revision = '22c72312df28'
down_revision = '25ecbd961535'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    add_column_query = """
    alter table commits
    add column repo_id integer
    default NULL
    references repos (id);
    """
    query = """
    select repos.id, commits.id
    from repos
    inner join commits
    on repos.name=commits.repo_name
    """
    update_statement_template = """
    update commits
    set repo_id = {repo_id}
    where id = {commit_id}
    """

    engine = op.get_bind().engine
    results = engine.execute(query)
    results = [dict(zip(['repo_id', 'commit_id'], row)) for row in results]

    # This is broken for sqlite (as far as I can see).
    #op.add_column('commits',
    #              sa.Column(
    #                  'repo_id',
    #                  sa.INTEGER,
    #                  sa.ForeignKey('repos.id'),
    #                  server_default=None,
    #              ))
    engine.execute(add_column_query)
    for result in results:
        update_statement = update_statement_template.format(**result)
        engine.execute(text(update_statement))

    # This is also broken for sqlite.. :/  You can't drop columns.
    #op.drop_column('commits', 'repo_name')

def downgrade():
    pass
