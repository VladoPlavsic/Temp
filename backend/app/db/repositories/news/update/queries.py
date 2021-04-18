from app.db.repositories.parsers import list_to_string

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