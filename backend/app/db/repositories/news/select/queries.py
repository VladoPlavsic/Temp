def select_all_news_query() -> str:
    return \
        f"SELECT (news.select_all_master_news()).*"

def select_all_news_images_query() -> str:
    return \
        f"SELECT (news.select_all_slave_news()).*"