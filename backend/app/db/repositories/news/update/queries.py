import json

from app.db.repositories.parsers import list_to_string, string_or_null

def update_news_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT news.update_news_sharing_links('{{{keys}}}', '{{{links}}}')"

def update_news_images_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT news.update_news_images_sharing_links('{{{keys}}}', '{{{links}}}')"

def update_news_metadata_query(id: int, date: str, title: str, short_desc: str, content: str, object_key: str, preview_image_url: str, images: list) -> str:
    return  (
        f"UPDATE news.news SET (date, title, short_desc, content, object_key, preview_image_url, images) = ('{date or ''}', '{title or ''}', '{short_desc or ''}', '{content or ''}', '{object_key or '-'}', '{preview_image_url or ''}', '{json.dumps(images or [])}'::JSONB) WHERE id={id} RETURNING *"
    )
