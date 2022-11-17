"""Change news structure

Revision ID: d28521eab86d
Revises: 31a9c087db12
Create Date: 2022-11-17 11:21:02.300924
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'd28521eab86d'
down_revision = '31a9c087db12'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('''
    ALTER TABLE "news"."news"
        DROP COLUMN "url",
        ADD COLUMN "images" JSONB NOT NULL DEFAULT '[]'::JSONB
    ;
    ''')

def downgrade() -> None:
    op.execute('''
    ALTER TABLE "news"."news"
        ADD COLUMN "url" TEXT,
        DROP COLUMN "images"
    ;
    ''')
