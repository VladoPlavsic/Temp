"""create cources
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
    CREATE TABLE "public"."cources" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "title" VARCHAR(100) COLLATE "en_US" NOT NULL CHECK("title" ~ '\S+'),
        "image" TEXT,
        "object_key" text NOT NULL,
        "created" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updated" TIMESTAMP NOT NULL DEFAULT NOW()
    )
    """)

def downgrade() -> None:
    op.execute('DROP TABLE "public"."cources"')
