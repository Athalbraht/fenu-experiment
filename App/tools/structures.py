# tools/structures.py

import config
from App.models import Topics, Anwsers
from datetime import datetime as dt

class ForumStruct():
    def __init__(self):
        self.set_sections()

    def get_anwsers(self, topic_id):
        ans = Anwsers.query.filter(Anwsers.topic==topic_id).all()
        if len(ans)==0:
            return [Anwsers()]
        else:
            return ans

    def get_thread(self, topic_id):
        return {"anwsers"   : self.get_anwsers(topic_id),
                "question"  : Topics.query.filter(Topics.id==topic_id).first()}

    def set_sections(self):
        _dic = {}
        iid = 0
        for category in config.FORUM_CATEGORIES.keys():
            _dic[category] = {}
            for section in config.FORUM_CATEGORIES[category]:
                _dic[category][section] = {}
                _category = "{}:{}".format(category,section)
                _topics = Topics.query.filter(Topics.category==_category)
                _anwsers = Anwsers.query.filter(Anwsers.category==_category)
                _dic[category][section]["category"] = _category
                _tab = []
                for _topic in _topics.all():
                    _tab.append({"question":_topic, "anwsers":self.get_anwsers(_topic.id)})
                _dic[category][section]["id"] = str(iid)
                iid += 1
                _dic[category][section]["topics"] = _tab
                _dic[category][section]["n_topics"] = len(_dic[category][section]["topics"])
                _dic[category][section]["n_anwsers"] = len(_anwsers.all())
                _dic[category][section]["last_topic"] = _topics.order_by(Topics.timestamp.desc()).first()
                _dic[category][section]["last_anwser"] =_anwsers.order_by(Anwsers.timestamp.desc()).first()
        self.forum_sections = {}
        self.forum_sections.update(_dic)
