from dataclasses import dataclass
from pymongo import MongoClient
from config import load_env, mongodb_conn_str
import re

_owner = 'owner'
_created = 'created'
_uuid = 'uuid'
_topic = 'topic'
_language = 'language'
_messages = 'messages'

def detect_language(string):
    language_codes = "en"

    chinese = re.compile(r'[\u4E00-\u9FFF]+')
    japanese = re.compile(r'[\u3040-\u30FF]+')

    if chinese.search(string):
        language_codes = "zh"
    if japanese.search(string):
        language_codes = "ja"

    return language_codes

@dataclass(frozen=True)
class User:
    name: str
    full_name: str

@dataclass(frozen=True)
class ConversationInfo:
    uuid: str
    topic: str
    language: str

class Storage:
    def __init__(self):
        self.client = MongoClient(mongodb_conn_str())
        self.db = self.client.MyChatGPT
        self.app_collection = self.db.app
        self.qa_collection = self.db.QA
        self.settings_collection = self.db.settings
    
    def get_history(self,user: User, min_msg:int, limit: int, skip: int):
        result = self.qa_collection.aggregate([
            {
                '$match': {_owner: user.name}
            },
            {
                '$sort': {_created: -1}
            },
            {
                '$project': {
                    _uuid: 1,
                    _topic: 1,
                    _language: 1,
                    'msgCount': {'$size': f'${_messages}'}
                }
            },
            {
                '$match': {
                    'msgCount': {'$gt': min_msg}
                }
            },
            {'$skip': skip},
            {'$limit': limit}
        ])
        return (ConversationInfo(r[_uuid],r[_topic],detect_language(r[_topic])) for r in result)

if __name__ == '__main__':
    load_env()
    s = Storage()
    for i in s.get_history(User('mu','Mu Lu'),1,10,0):
        print(i)
