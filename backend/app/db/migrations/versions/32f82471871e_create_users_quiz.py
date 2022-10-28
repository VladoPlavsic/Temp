"""Create users_quiz
Revision ID: 32f82471871e
Revises: 68c939692fc4
Create Date: 2022-10-28 07:49:47.659536
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '32f82471871e'
down_revision = '68c939692fc4'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE "private"."users_quiz" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "quiz_id" INT4 NOT NULL,
        "user_id" INT4 NOT NULL
    );
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE "private"."users_quiz";
    """)
