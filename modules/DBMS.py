from logging import exception
from pymongo import MongoClient


class DataBase:
    def __init__(self):
        self.DBClient = MongoClient('mongodb://localhost:27017/')
        self.CRDB = self.DBClient.CrawlerDB
        self.CRCollection = self.CRDB.CrawlerCollection
        self.URLDB = self.DBClient.URLDB
        self.URLCollection = self.URLDB.URLCollection

    def addToContentRepository(self, keys, values):
        dataDict = dict(zip(keys, values))
        success = self.CRCollection.insert_one(dataDict)
        return success

    def listContentRepository(self, key, value):
        data = self.CRCollection.find({key, value})
        return data

    def deleteFromContentRepository(self, id):
        success = self.CRCollection.remove({'_id': id})
        return success

    def addToURLStore(self, values):
        keys = len(values) * ["URL", ]
        dataDict = [{k: v} for k, v in zip(keys, values)]
        print("dataDict: ", dataDict)
        success = self.URLCollection.insert_many(dataDict)
        return success

    def listURLStore(self, key, value):
        data = self.URLCollection.find({key, value})
        return data

    def getFirstURL(self):
        data = self.URLCollection.find_one()
        return data

    def deleteFromURLStore(self, id):
        success = self.URLCollection.remove({'_id': id})
        return success

    def getURLID(self, URL):
        data = self.URLCollection.find_one({'URL': URL})
        return data['_id']
