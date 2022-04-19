from threading import Thread
from modules.DBMS import DataBase
import modules.Crawler as Crawler
import modules.Parser as Parser
import modules.Indexer as Indexer
from datetime import datetime
from timeit import timeit
import os
import pickle
import psutil

global threadList
global DB

global AvgTime


def main():
    global AvgTime
    global threadList
    AvailThreads = psutil.cpu_count()
    URLList = DB.getXUrls(AvailThreads)
    for URL in URLList:
        startThreadAtURL(URL['URL'])
        DB.deleteFromURLStore(URL['_id'])
    for thread in threadList:
        thread.join()
    while len(threadList) > 0:
        for thread in threadList:
            if not thread.is_alive():
                setAvgTime(AvgTime)
                threadList.remove(thread)
                nextURL = DB.getFirstURL()
                if nextURL is not None:
                    startThreadAtURL(nextURL['URL'])
                    threadList[-1].join()
    return True


def startThreadAtURL(crawlURL):
    try:
        global threadList
        newThread = Thread(target=process, args=(crawlURL,))
        threadList.append(newThread)
        newThread.start()
        return True
    except Exception as e:
        print(e)
        return False


def process(crawlURL):
    try:
        global AvgTime
        start = datetime.now()
        print(
            "Starting to crawl on {URL} at {Time}".format(URL=crawlURL, Time=start))
        crawlResults = Crawler.crawl(crawlURL)
        # print("Finished crawling on {URL} at {Time}".format(
        #     URL=crawlURL, Time=datetime.now()))
        if crawlResults is None:
            return False
        parseResults = Parser.parse(crawlResults)
        # print("Finished parsing on {URL} at {Time}".format(
        #     URL=crawlURL, Time=datetime.now()))
        if parseResults is None:
            return False
        indexResults = Indexer.index(parseResults, crawlURL, DB)
        # print("Finished indexing on {URL} at {Time}".format(
        #     URL=crawlURL, Time=datetime.now()))
        Indexer.appendURLs(crawlURL, crawlResults, DB)
        # print(crawlResults, parseResults, indexResults)
        end = datetime.now()
        print("Time taken for {URL}: {Time}".format(
            URL=crawlURL, Time=end-start))
        AvgTime['Time'] = ((AvgTime['Time'] * AvgTime['Count']) + (end-start).days) / (AvgTime['Count'] + 1)
        AvgTime['Count'] += 1
        return True
    except Exception as e:
        print(e)
        return False


def getAvgTime():
    AvgTime = {'Time': 0, 'Count': 0}
    try:
        if os.path.exists(os.getcwd() + "/AvgTime.data"):
            TimeFile = open(os.getcwd() + "/AvgTime.data", 'rb')
            AvgTime = pickle.load(TimeFile)
            TimeFile.close()
    except Exception as e:
        print(e)
    finally:
        print("Average time taken: {Time}".format(Time=AvgTime['Time']))
        return AvgTime


def setAvgTime(AvgTime):
    try:
        TimeFile = open(os.getcwd() + "/AvgTime.data", 'wb')
        pickle.dump(AvgTime, TimeFile)
        TimeFile.close()
    except Exception as e:
        print(e)
    finally:
        print("Average time taken: {Time}".format(Time=AvgTime['Time']))
        return True

if __name__ == '__main__':
    DB = DataBase()
    threadList = []
    AvgTime = getAvgTime()
    while True:
        main()
    print("Exited at {Time}".format(Time=datetime.now()))
