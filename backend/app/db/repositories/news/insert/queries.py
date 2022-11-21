import json

from app.db.repositories.parsers import string_or_null

def insert_news_check_query(date, url) -> str:
    return \
        f"SELECT (news.check_if_news_can_be_created({string_or_null(date, url)})) AS yes"

def insert_news_master_query(date, title, short_desc, content, object_key, preview_image_url, images) -> str:
    js1 = json.dumps(images or []).replace("'", "''")
    return (
        f"INSERT INTO news.news (date, title, short_desc, content, object_key, preview_image_url, images) VALUES ({string_or_null(date, title, short_desc, content, object_key, preview_image_url)}, '{js1}'::JSONB) RETURNING *"
    )

def insert_news_slave_query(fk, medium) -> str:
    orders, urls, keys = map(list, zip( *((media.order, media.url, media.object_key) for media in medium)))

    orders = ','.join(map(str,orders))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    return \
        f"SELECT (news.insert_news_slave({fk}, '{{{orders}}}'::int[], '{{{keys}}}', '{{{urls}}}')).*"
