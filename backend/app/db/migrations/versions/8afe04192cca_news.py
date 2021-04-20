"""News
Revision ID: 8afe04192cca
Revises: 91c0fe2ebacf
Create Date: 2021-04-08 15:50:08.915693
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '8afe04192cca'
down_revision = '91c0fe2ebacf'
branch_labels = None
depends_on = None

def create_tables() -> None:
    # master table
    op.create_table(
        'news',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Text, nullable=False),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('short_desc', sa.Text, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('url', sa.Text, nullable=False),
        sa.Column('cloud_key', sa.Text, nullable=False),
        sa.Column('preview_image_url', sa.Text, nullable=False),
        schema='news'
    )
    # slave table
    op.create_table(
        'news_images',
        sa.Column('fk', sa.Integer, nullable=False),
        sa.Column('order', sa.Integer, nullable=False),
        sa.Column('cloud_key', sa.Text, nullable=False),
        sa.Column('url', sa.Text, nullable=False),
        sa.UniqueConstraint('fk', 'order'),
        sa.ForeignKeyConstraint(['fk'], ['news.news.id'], onupdate='CASCADE', ondelete='CASCADE'),
        schema='news',
    )

def create_news_functions() -> None:
    # insert news master
    op.execute("""
    CREATE OR REPLACE FUNCTION news.insert_news_master(i_date TEXT, i_title TEXT, i_short_desc TEXT , i_content TEXT, i_url TEXT, i_cloud_key TEXT, i_preview_image_url TEXT)
    RETURNS TABLE (id int, date text, title text, short_desc text, content text, url text, cloud_key text, preview_image_url text)
    AS $$
    DECLARE 
        inserted_id int;
    BEGIN
        INSERT INTO news.news (date, title, short_desc, content, url, cloud_key, preview_image_url)
        VALUES (i_date, i_title, i_short_desc, i_content, i_url, i_cloud_key, i_preview_image_url) RETURNING news.news.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM news.news WHERE news.news.id = inserted_id);
    END $$ LANGUAGE plpgsql
    """)
    # insert news slave
    op.execute("""
    CREATE OR REPLACE FUNCTION news.insert_news_slave(i_fk int, i_orders int[], i_keys text[], i_urls text[])
    RETURNS TABLE (fk int, "order" int, cloud_key text, url text)
    AS $$ 
    BEGIN
        INSERT INTO news.news_images (fk, "order", cloud_key, url)
        SELECT i_fk, unnest(i_orders), unnest(i_keys), unnest(i_urls);
        RETURN QUERY (SELECT * FROM news.news_images WHERE news.news_images.fk = i_fk);
    END $$ LANGUAGE plpgsql;
    """)

    # select news master
    op.execute("""
    CREATE OR REPLACE FUNCTION news.select_master_news(i_offset int, i_limit int)
    RETURNS TABLE (id int, date text, title text, short_desc text, content text, url text, cloud_key text, preview_image_url text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM news.news ORDER BY id LIMIT i_limit OFFSET i_offset);
    END $$ LANGUAGE plpgsql
    """)
    # select news slave
    op.execute("""
    CREATE OR REPLACE FUNCTION news.select_salve_news(i_fk int)
    RETURNS TABLE (fk int, "order" int, cloud_key text, url text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM news.news_images WHERE news.news_images.fk = i_fk ORDER BY "order");
    END $$ LANGUAGE plpgsql
    """)
    # select all news master for updating
    op.execute("""
    CREATE OR REPLACE FUNCTION news.select_all_master_news()
    RETURNS TABLE (id int, cloud_key text)
    AS $$
    BEGIN 
        RETURN QUERY (SELECT news.news.id, news.news.cloud_key FROM news.news);
    END $$ LANGUAGE plpgsql;
    """)
    # select all news slaves for updating
    op.execute("""
    CREATE OR REPLACE FUNCTION news.select_all_slave_news()
    RETURNS TABLE ("order" int, cloud_key text)
    AS $$
    BEGIN
        RETURN QUERY (SELECT news.news_images."order", news.news_images.cloud_key FROM news.news_images);
    END $$ LANGUAGE plpgsql;
    """)

    # delete news
    op.execute("""
    CREATE OR REPLACE FUNCTION news.delete_news(i_id int)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM news.news WHERE id = i_id;
    END $$ LANGUAGE plpgsql
    """)

    # update news master links
    op.execute("""
    CREATE OR REPLACE FUNCTION news.update_news_sharing_links(cloud_keys text[], preview_image_urls text[])
    RETURNS VOID
    AS $$
    BEGIN
    FOR index IN 1 .. array_upper(cloud_keys, 1)
    LOOP 
        UPDATE news.news SET
        preview_image_url = preview_image_urls[index]
        WHERE cloud_key = cloud_keys[index];
    END LOOP;
    END $$ LANGUAGE plpgsql
    """)
    # update news slave links
    op.execute("""
    CREATE OR REPLACE FUNCTION news.update_news_images_sharing_links(cloud_keys text[], urls text[])
    RETURNS VOID
    AS $$
    BEGIN
    FOR index IN 1 .. array_upper(cloud_keys, 1)
    LOOP 
        UPDATE news.news_images SET
        url = urls[index]
        WHERE cloud_key = cloud_keys[index];
    END LOOP;
    END $$ LANGUAGE plpgsql;
    """)


def drop_tables() -> None:
    op.execute('DROP TABLE news.news_images')
    op.execute('DROP TABLE news.news')

def drop_functions() -> None:
    functions = [
        'insert_news_master',
        'insert_news_slave',
        'select_master_news',
        'select_salve_news',
        'select_all_master_news',
        'select_all_slave_news',
        'delete_news',
        'update_news_sharing_links',
        'update_news_images_sharing_links',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION news.{function}")


def upgrade() -> None:
    create_tables()
    create_news_functions()

def downgrade() -> None:
    drop_tables()
    drop_functions()