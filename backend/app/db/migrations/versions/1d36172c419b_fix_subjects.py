"""Fix subjects
Revision ID: 1d36172c419b
Revises: 420a5ec92fd8
Create Date: 2022-10-22 12:52:45.187282
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '1d36172c419b'
down_revision = '420a5ec92fd8'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    INSERT INTO private.subject (id, fk, name_en, name_ru, background, object_key, order_number) VALUES (1, 1, 'Fix', 'Костыль', 'https://storage.yandexcloud.net/mpei-production/subscription/10klass/shubham-sharan-z-fq3wbvfmu-unsplash.jpg?AWSAccessKeyId=rUapbMUCujqhRIsxcDUV&Signature=3%2BHU8s6mIIWl5oLFSdgXUQb1he0%3D&Expires=1666644061', 'subscription/10klass/shubham-sharan-z-fq3wbvfmu-unsplash.jpg', 1);
    """)

def downgrade() -> None:
    op.execute("DELETE FROM private.subject WHERE id=1")
