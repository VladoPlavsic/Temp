"""Add objet_key
Revision ID: 1f4e7151f23a
Revises: 7122d2f13884
Create Date: 2022-11-12 11:08:28.572383
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '1f4e7151f23a'
down_revision = '7122d2f13884'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('''
    ALTER TABLE "private"."blocks"
        ADD COLUMN "object_key" TEXT
    ;
    ''')

def downgrade() -> None:
    op.execute('''
    ALTER TABLE "private"."blocks"
        DROP COLUMN "object_key"
    ;
    ''')
