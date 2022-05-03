"""jwt_to_headers
Revision ID: a18ff258a32c
Revises: db420b27b5a1
Create Date: 2022-05-03 12:35:14.282654
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'a18ff258a32c'
down_revision = 'db420b27b5a1'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # set jwt token
    op.execute(
    """
    CREATE OR REPLACE FUNCTION users.remove_jwt(user_id int)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.users SET
            jwt_token = NULL
        WHERE users.users.id = user_id;
    END $$ LANGUAGE plpgsql;
    """)

def downgrade() -> None:
    op.execute("""DROP FUNCTION users.remove_jwt(user_id int)""")