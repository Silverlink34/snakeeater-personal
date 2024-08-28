import schedule
import time
from dotenv import load_dotenv
from os import getenv, path
from redis import ConnectionPool
from redis import Redis
from datetime import datetime
from PyRSS2Gen import RSS2, RSSItem, Guid
import json
import pdb

xml_base_folder = "/rss/"

def load_envs():
    load_dotenv()
    global redis_host
    global redis_port
    global delimiter_override
    global article_key_prefix
    global schedule_interval_minutes
    global article_1_category 
    global article_2_category 
    global article_3_category 
    global article_4_category 
    global article_5_category 
    global article_6_category 
    global article_7_category 
    global article_8_category 
    global article_9_category 
    global article_10_category
    global article_1_keywords 
    global article_2_keywords 
    global article_3_keywords 
    global article_4_keywords 
    global article_5_keywords 
    global article_6_keywords 
    global article_7_keywords 
    global article_8_keywords 
    global article_9_keywords 
    global article_10_keywords
    global articles_dict
    redis_host = getenv("REDIS_HOST")
    redis_port = getenv("REDIS_PORT")
    #
    delimiter_override = getenv("DELIMTER_OVERRIDE")
    article_key_prefix = getenv("ARTICLE_KEY_PREFIX")
    if not delimiter_override:
        delimiter_override = ","
    if not article_key_prefix:
        article_key_prefix = ""
    #
    schedule_interval_minutes = int(getenv("SCHEDULE_INTERVAL_MINUTES"))
    article_1_category = getenv("ARTICLE_1_CATEGORY")
    article_2_category = getenv("ARTICLE_2_CATEGORY")
    article_3_category = getenv("ARTICLE_3_CATEGORY")
    article_4_category = getenv("ARTICLE_4_CATEGORY")
    article_5_category = getenv("ARTICLE_5_CATEGORY")
    article_6_category = getenv("ARTICLE_6_CATEGORY")
    article_7_category = getenv("ARTICLE_7_CATEGORY")
    article_8_category = getenv("ARTICLE_8_CATEGORY")
    article_9_category = getenv("ARTICLE_9_CATEGORY")
    article_10_category = getenv("ARTICLE_10_CATEGORY")
    article_1_keywords = getenv("ARTICLE_1_KEYWORDS")
    article_2_keywords = getenv("ARTICLE_2_KEYWORDS")
    article_3_keywords = getenv("ARTICLE_3_KEYWORDS")
    article_4_keywords = getenv("ARTICLE_4_KEYWORDS")
    article_5_keywords = getenv("ARTICLE_5_KEYWORDS")
    article_6_keywords = getenv("ARTICLE_6_KEYWORDS")
    article_7_keywords = getenv("ARTICLE_7_KEYWORDS")
    article_8_keywords = getenv("ARTICLE_8_KEYWORDS")
    article_9_keywords = getenv("ARTICLE_9_KEYWORDS")
    article_10_keywords = getenv("ARTICLE_10_KEYWORDS")
    all_categories = [article_1_category, article_2_category, article_3_category, article_4_category, article_5_category, article_6_category, article_7_category, article_8_category, article_9_category, article_10_category]
    all_keyword_strings = [article_1_keywords, article_2_keywords, article_3_keywords, article_4_keywords, article_5_keywords, article_6_keywords, article_7_keywords, article_8_keywords, article_9_keywords, article_10_keywords]
    articles_dict = {}
    for i in range(len(all_categories)):
        category = all_categories[i]
        if category:
            keywords_string = all_keyword_strings[i]
            if keywords_string:
                articles_dict[category] = {}
                articles_dict[category]["keywords"] = keywords_string.split(delimiter_override)

def user_set_vars():
    if redis_host and redis_port and article_1_keywords:
        return True
    else:
        return False

def cleanup_wierd_chars_in_string(stringToClean):
    cleaned_up_string = ""
    if stringToClean:
        import re
        #cleaned_up_string = stringToClean.replace("’","'").replace("‘","'")
        #cleaned_up_string = re.sub(r'[^\x00-\x7F]+', '', stringToClean)
        cleaned_up_string = stringToClean.encode("utf-8",errors="replace").decode("utf-8", errors="replace")
        cleaned_up_string = re.sub(r'[^\x00-\x7F]+', '', stringToClean)
    return cleaned_up_string

def get_redis_data_and_post_rss_xmls_job():
    redis_db = Redis(host=redis_host, port=redis_port, decode_responses=True)
    for category in articles_dict.keys():
        category_spaces_replaced = category.replace(" ","_")
        rss_items = []
        for keyword in articles_dict[category]["keywords"]:
            redis_articles_dict_list = redis_db.smembers(article_key_prefix+keyword)
            for redis_article_dict in redis_articles_dict_list:
                redis_article_dict = json.loads(redis_article_dict)
                rss_item = RSSItem(
                    title=cleanup_wierd_chars_in_string(redis_article_dict["title"]),
                    link=redis_article_dict["url"],
                    description=cleanup_wierd_chars_in_string(redis_article_dict["description"]),
                    guid=Guid(redis_article_dict["url"]),
                    pubDate=datetime.strptime(redis_article_dict["publishedAt"], "%Y-%m-%dT%H:%M:%S%z"))
                rss_items.append(rss_item)
        rss = RSS2(
            title = category + " RSS Feed",
            link = "http://snakeEaterHostname/"+category_spaces_replaced+".xml",
            description = "a RSS feed of articles for "+category,
            lastBuildDate = datetime.now(),
            items = rss_items)
        with open(xml_base_folder+category_spaces_replaced+".xml", "w") as f:
            try:
                rss.write_xml(f)
            except UnicodeEncodeError:
                print("There was a character error while trying to write: "+xml_base_folder+category_spaces_replaced+".xml. Skipping.")
                for rss_item in rss_items:
                    print(rss_item.title)
                    print(rss_item.description)
                pdb.set_trace()
                continue
            except AttributeError:
                print("attribute error.")
                pdb.set_trace()
        print("---")
        print("Generated: "+xml_base_folder+category_spaces_replaced+".xml.")
        print("Can be accessed at: http://snakeEaterHostname:81/"+xml_base_folder+category_spaces_replaced+".xml")

#start
load_envs()
if not user_set_vars():
    print("You did not set one of the three variables in the .env file!!!")
    print("REDIS_HOST, REDIS_PORT, or ARTICLE_1_KEYWORDS !")

get_redis_data_and_post_rss_xmls_job()

schedule.every(schedule_interval_minutes).minutes.do(get_redis_data_and_post_rss_xmls_job)
while True:
    schedule.run_pending()
    time.sleep(1)