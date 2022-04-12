from threading import Thread
from modules.DBMS import DataBase
import modules.Crawler as Crawler
import modules.Parser as Parser
import modules.Indexer as Indexer
from datetime import datetime
from timeit import timeit

threadList = []
global DB


def main():
    URL = DB.getFirstURL()
    if URL == None:
        return False
    startThreadAtURL(URL['URL'])
    return True


def startThreadAtURL(crawlURL):
    try:
        newThread = Thread(target=process, args=(crawlURL,))
        threadList.append(newThread)
        print(
            "Starting to crawl on {URL} at {Time}".format(URL=crawlURL, Time=datetime.now()))
        newThread.start()
        newThread.join()
        return True
    except Exception as e:
        print(e)
        return False


def process(crawlURL):
    try:
        start = datetime.now()
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
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    DB = DataBase()
    while True:
        main()
    print("Exited at {Time}".format(Time=datetime.now()))
