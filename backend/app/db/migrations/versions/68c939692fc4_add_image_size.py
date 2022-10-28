"""Add image_size
Revision ID: 68c939692fc4
Revises: 9ba1351bde53
Create Date: 2022-10-28 06:30:01.725493
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '68c939692fc4'
down_revision = '9ba1351bde53'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('''
    ALTER TABLE "private"."quiz"
        ADD COLUMN "image_size" TEXT
    ;
    ''')

def downgrade() -> None:
    op.execute('''
    ALTER TABLE "private"."quiz"
        DROP COLUMN "image_size"
    ;
    ''')

