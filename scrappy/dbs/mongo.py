# coding:utf8
__author__ = 'modm'
from pymongo import MongoClient, errors, DESCENDING
import datetime
from scrapy.utils import project


class MongoDBClient(object):
    def __init__(self, collection_name):
        self.settings = project.get_project_settings()  # get settings
        self.MONGO_URL = self.settings.get("MONGO_URL", "localhost")
        self.client = MongoClient(
            host=self.mongo_url, tz_aware=True)
        self.db = self.client['crawl_db']
        self.posts = self.db[collection_name]

    def storeContent(self, content):
        content['created_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            post_id = self.posts.insert(content)
            return post_id
        except errors.DuplicateKeyError, e:
            raise Exception('err', 'DuplicateKeyError')

    def findOne(self, conditionDict):
        return self.posts.find_one(conditionDict)

    def findOneBySort(self, conditionDict, sortTuple):
        try:
            collections = self.posts.find(conditionDict).sort([sortTuple])
            return collections[0] if collections else None
        except:
            return None

    def findAll(self, conditionDict):
        for post in self.posts.find(conditionDict).batch_size(30):
            yield post

    def findAndUpdate(self, queryDict, updateDict, sort=None):
        if sort:
            return self.posts.find_and_modify(query=queryDict, update={"$set": updateDict}, sort=sort, upsert=False,
                                              full_response=True)['value']
        else:
            return \
                self.posts.find_and_modify(query=queryDict, update={"$set": updateDict}, upsert=False,
                                           full_response=True)[
                    'value']

    def updateContent(self, conditionDict, setsDicts, upsert=False, multi=False):
        if multi:
            self.posts.update_many(conditionDict, {"$set": setsDicts}, upsert=upsert)
        else:
            self.posts.update_one(conditionDict, {"$set": setsDicts}, upsert=upsert)

    def updateContentFree(self, conditionDict, updateDict):
        if "$set" not in updateDict:
            raise Exception("are you series?")
        self.posts.update(conditionDict, updateDict, upsert=False)

    def count(self, conditionDict):
        return self.posts.count(conditionDict)

    def close(self):
        self.client.close()

    def getPosts(self):
        return self.posts


class MonogoDBHelper():
    instanceDict = {}

    def __init__(self, collection_name):
        self.mongo = MongoDBClient(collection_name)

    @classmethod
    def getInstance(cls, collection_name):
        if collection_name in cls.instanceDict:
            return cls.instanceDict[collection_name]
        else:
            cls.instanceDict[collection_name] = cls(collection_name)
            return cls.instanceDict[collection_name]

    def isExistById(self, id):
        if self.mongo.findOne({'_id': id}):
            return True
        else:
            return False

    def isExist(self, queryCondition):
        if self.mongo.findOne(queryCondition):
            return True
        else:
            return False

    def findOne(self, condition):
        return self.mongo.findOne(condition)

    def findAll(self, condition):
        return self.mongo.findAll(condition)

    def update(self, queryCondition, updateCondition, multi=False):
        self.mongo.updateContent(queryCondition, updateCondition, multi=multi)

    def getClient(self):
        return self.mongo
