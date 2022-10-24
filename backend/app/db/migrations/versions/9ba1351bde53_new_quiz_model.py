"""New quiz model
Revision ID: 9ba1351bde53
Revises: 1d36172c419b
Create Date: 2022-10-24 12:50:46.057229
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '9ba1351bde53'
down_revision = '1d36172c419b'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE "private"."quiz" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "fk" INT4 NOT NULL,
        "order_number" INT4 NOT NULL,
        "question_type" TEXT,
        "question" TEXT,
        "object_key" TEXT,
        "image_url" TEXT,
        "answers" JSONB NOT NULL DEFAULT '[]'::JSONB,
        "options" JSONB NOT NULL DEFAULT '[]'::JSONB,
        "created" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updated" TIMESTAMP NOT NULL DEFAULT NOW(),
        CONSTRAINT "quiz_questions_fk_fkey" FOREIGN KEY ("fk") REFERENCES "private"."lecture"("id") ON DELETE CASCADE ON UPDATE CASCADE
    );
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE "private"."quiz";
    """)
