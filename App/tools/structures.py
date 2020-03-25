# tools/structures.py

import config
from App.models import Topics, Anwsers
from datetime import datetime as dt

class ForumStruct():
    def __init__(self):
        self.set_sections()
        self.new_anwsers = self._new_anwsers1()
        self.new_threads = self._new_threads1()
        self.without_anwser = self._without_anwser1()

    def _new_anwsers1(self, n=2):
        _new = Anwsers.query.order_by(Anwsers.timestamp.desc()).all()[:n]
        return _new

    def _without_anwser1(self):
        _all = Topics.query.all()
        _empty = [ ]
        for topic in _all:
            if len(Anwsers.query.filter(Anwsers.topic==topic.id).all()) == 0:
                _empty.append(topic)
        return _empty

    def _new_threads1(self,n=2):
        _new = Topics.query.order_by(Topics.timestamp.desc()).all()[:n]
        return _new

    def get_anwsers(self, topic_id):
        ans = Anwsers.query.filter(Anwsers.topic==topic_id).all()
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
                    _ans = self.get_anwsers(_topic.id)
                    _tab.append({"question":_topic, "anwsers":_ans, "n_anwsers":len(_ans)})
                _dic[category][section]["id"] = str(iid)
                iid += 1
                _dic[category][section]["topics"] = _tab
                _dic[category][section]["n_topics"] = len(_dic[category][section]["topics"])
                _dic[category][section]["n_anwsers"] = len(_anwsers.all())
                _dic[category][section]["last_topic"] = _topics.order_by(Topics.timestamp.desc()).first()
                _dic[category][section]["last_anwser"] =_anwsers.order_by(Anwsers.timestamp.desc()).first()
        self.forum_sections = {}
        self.forum_sections.update(_dic)
