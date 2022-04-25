from threading import Thread
from modules.DBMS import DataBase
import modules.Crawler as Crawler
import modules.Parser as Parser
import modules.Indexer as Indexer
from datetime import datetime
import psutil

global threadList
global DB


def main():
    try:
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
                    threadList.remove(thread)
                    nextURL = DB.getFirstURL()
                    if nextURL is not None:
                        startThreadAtURL(nextURL['URL'])
                        threadList[-1].join()
    except Exception as e:
        print(e)
    finally:
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
        start = datetime.now()
        print(
            "Starting to crawl on {URL} at {Time}".format(URL=crawlURL, Time=start))
        crawlResults = Crawler.crawl(crawlURL)
        if crawlResults is None:
            return False
        parseResults = Parser.parse(crawlResults)
        if parseResults is None:
            return False
        indexResults = Indexer.index(parseResults, crawlURL, DB)
        Indexer.appendURLs(crawlURL, crawlResults, DB)
        end = datetime.now()
        print("Time taken for {URL}: {Time}".format(
            URL=crawlURL, Time=end-start))
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    DB = DataBase()
    threadList = []
    while True:
        main()
    print("Exited at {Time}".format(Time=datetime.now()))
