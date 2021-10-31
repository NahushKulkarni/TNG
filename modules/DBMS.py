from pymongo import MongoClient


class DataBase:
    def __init__(self):
        self.DBClient = MongoClient('mongodb://localhost:27017/')
        self.CRDB = self.DBClient.CrawlerDB
        self.CRCollection = self.CRDB.CrawlerCollection
        self.URLDB = self.DBClient.URLDB
        self.URLCollection = self.URLDB.URLCollection

    def addToContentRepository(keys, values, self):
        dataDict = zip(keys, values)
        success = self.CRCollection.insert(dataDict)
        return success

    def listContentRepository(key, value, self):
        data = self.CRCollection.find({key, value})
        return data

    def deleteFromContentRepository(id, self):
        success = self.CRCollection.remove({'_id': id})
        return success

    def addToURLStore(keys, values, self):
        dataDict = zip(keys, values)
        success = self.URLCollection.insert(dataDict)
        return success

    def listURLStore(key, value, self):
        data = self.URLCollection.find({key, value})
        return data

    def getFirstURL(self):
        data = self.URLCollection.find_one()
        return data

    def deleteFromURLStore(id, self):
        success = self.URLCollection.remove({'_id': id})
        return success
