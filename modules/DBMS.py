from pymongo import MongoClient


class DataBase:
    def __init__(self):
        self.DBClient = MongoClient('mongodb://localhost:27017/')
        self.CRDB = self.DBClient.CrawlerDB
        self.CRCollection = self.CRDB.CrawlerCollection
        self.URLDB = self.DBClient.URLDB
        self.URLCollection = self.URLDB.URLCollection

    def addToContentRepository(self, keys, values):
        dataDict = zip(keys, values)
        success = self.CRCollection.insert(dataDict)
        return success

    def listContentRepository(self, key, value):
        data = self.CRCollection.find({key, value})
        return data

    def deleteFromContentRepository(self, id):
        success = self.CRCollection.remove({'_id': id})
        return success

    def addToURLStore(self, values):
        keys = len(values) * ["URL", ]
        dataDict = dict(zip(keys, values))
        print("addToURLStore: ", dataDict)
        success = self.URLCollection.insert(dataDict)
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
