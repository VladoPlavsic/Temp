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
    INSERT INTO private.grade (id, name_en, name_ru, background, object_key, order_number) VALUES (1, 'Fix', 'Костыль', 'https://eduplat.storage.yandexcloud.net/courses/b16319aa-faea-46ff-9f4b-b9796c432fff/128/blocks/theory/0691f069-5875-481e-8b34-71773dc6cb4c/%D1%81.png', 'courses/b16319aa-faea-46ff-9f4b-b9796c432fff/128/blocks/theory/0691f069-5875-481e-8b34-71773dc6cb4c/с.png', 1);
    """)

def downgrade() -> None:
    op.execute("DELETE FROM private.grade WHERE id=1")
