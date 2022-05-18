"""why_did_i_remove_return_value_on_delete
Revision ID: 44e96467a71f
Revises: a18ff258a32c
Create Date: 2022-05-18 17:49:50.888923
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '44e96467a71f'
down_revision = 'a18ff258a32c'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("DROP FUNCTION about.delete_team_member")
    # delete team member
    op.execute('''
    CREATE OR REPLACE FUNCTION about.delete_team_member(id_ int)
    RETURNS TEXT
    AS $$
    DECLARE
        key TEXT;
    BEGIN
    DELETE FROM about.our_team WHERE id = id_ RETURNING object_key INTO key;
    RETURN key;
    END $$ LANGUAGE plpgsql;
    ''')

def downgrade() -> None:
    pass
