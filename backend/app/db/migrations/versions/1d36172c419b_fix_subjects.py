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
    INSERT INTO private.subject (id, fk, name_en, name_ru, background, object_key, order_number) VALUES (1, 1, 'Fix', 'Костыль', 'https://eduplat.storage.yandexcloud.net/courses/b16319aa-faea-46ff-9f4b-b9796c432fff/128/blocks/theory/0691f069-5875-481e-8b34-71773dc6cb4c/%D1%81.png', 'courses/b16319aa-faea-46ff-9f4b-b9796c432fff/128/blocks/theory/0691f069-5875-481e-8b34-71773dc6cb4c/с.png', 1);
    """)

def downgrade() -> None:
    op.execute("DELETE FROM private.subject WHERE id=1")
