"""get all subjects without grade
Revision ID: 781f320fbf9d
Revises: 44e96467a71f
Create Date: 2022-10-16 15:26:50.433548
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '781f320fbf9d'
down_revision = '44e96467a71f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION private.select_all_subjects2()
        RETURNS TABLE (id int, fk int, name_en varchar(100), name_ru varchar(100), background text, object_key text, order_number int)
        AS $$
        BEGIN
        RETURN QUERY (SELECT * FROM private.subject ORDER BY private.subject.order_number);
        END $$ LANGUAGE plpgsql;
    """)

def downgrade() -> None:
    op.execute("DROP FUNCTION private.select_all_subjects2(int)")
