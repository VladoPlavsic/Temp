"""Fix grade data
Revision ID: 420a5ec92fd8
Revises: 781f320fbf9d
Create Date: 2022-10-21 08:18:52.298947
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '420a5ec92fd8'
down_revision = '781f320fbf9d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    INSERT INTO private.grade (id, name_en, name_ru, background, object_key, order_number) VALUES (1, 'Fix', 'Костыль', 'https://storage.yandexcloud.net/mpei-production/subscription/10klass/shubham-sharan-z-fq3wbvfmu-unsplash.jpg?AWSAccessKeyId=rUapbMUCujqhRIsxcDUV&Signature=3%2BHU8s6mIIWl5oLFSdgXUQb1he0%3D&Expires=1666644061', 'subscription/10klass/shubham-sharan-z-fq3wbvfmu-unsplash.jpg', 1);
    """)

def downgrade() -> None:
    op.execute("DELETE FROM private.grade WHERE id=1")
