"""Add order_number
Revision ID: 31a9c087db12
Revises: 1f4e7151f23a
Create Date: 2022-11-12 12:05:08.216455
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '31a9c087db12'
down_revision = '1f4e7151f23a'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('''
    ALTER TABLE "private"."blocks"
        ADD COLUMN "order_number" INT4
    ;
    ''')

def downgrade() -> None:
    op.execute('''
    ALTER TABLE "private"."blocks"
        DROP COLUMN "order_number"
    ;
    ''')
