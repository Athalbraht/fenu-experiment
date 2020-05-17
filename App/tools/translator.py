# tools/translator.py


'''
import config
from feedgen.feed import FeedGenerator

from App.models import *

def export_html(language, filename, content, index=False):
    if index:
        with open("{}/index.html".format(config.HOMEPAGE_FOLDER),"w") as html:
            html.write(content)
    else:
        with open("{}/{}/{}.html".format(config.HOMEPAGE_FOLDER, language, filename),"w") as html:
            html.write(content)
    return None

def get_rss(feeds_len):
    fg = FeedGenerator()
    fg.title(config.RSS["title"])
    fg.description(config.RSS["desc"])
    fg.link(href="{}/rss.xml".format(config.main["domain"]))
    feed = []
    posts = Posts.query.all()
    for item in posts[:feeds_len]:
        fe = fg.add_entry()
        fe.title("{} {}".format(item.head_pl, item.head_en))
        fe.description("{}\n\n{}".format(item.body_pl,item.body_en))
        fe.link(href="{}/rss.xml".format(config.main["domain"]))
        feed.append(fe)
    # return fg.rss_str(pretty=True).decode()
    print("Saving RSS file")
    fg.rss_file("{}/rss.xml".format(config.HOMEPAGE_FOLDER))
    return None
'''
