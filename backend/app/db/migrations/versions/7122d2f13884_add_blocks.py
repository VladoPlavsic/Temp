"""Add blocks
Revision ID: 7122d2f13884
Revises: 32f82471871e
Create Date: 2022-11-11 10:55:07.256867
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '7122d2f13884'
down_revision = '32f82471871e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE "private"."blocks" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "fk" INT4 NOT NULL,
        "type" TEXT NOT NULL,
        "heading" TEXT,
        "description" TEXT,
        "video" TEXT,
        "items" TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
        "questions" JSONB NOT NULL DEFAULT '[]'::JSONB
    );
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE "private"."blocks";
    """)
