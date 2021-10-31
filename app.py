from threading import Thread
from datetime import datetime
from modules.DBMS import DataBase
import modules.Crawler as Crawler
import modules.Parser as Parser
import modules.Indexer as Indexer
from datetime import datetime

threadList = []
global DB


def main():
    startThreadAtURL(DB.getFirstURL()['URL'])
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
        end = datetime.now()
        print("Crawling took {Time}".format(Time=end - start))
        print("Crawl Done")
        # print("====================================================================")
        # print(crawlResults['links'])
        # print("====================================================================")
        # print(crawlResults['meta'])
        # print("====================================================================")
        # print(crawlResults['images'])
        # print("====================================================================")
        # print(crawlResults['videos'])
        # print("====================================================================")
        # print(crawlResults['text'])
        # print("====================================================================")
        # print(crawlResults['headings'])
        parseResults = Parser.parse(crawlResults)
        print("Parse Done")
        print(parseResults)
        indexResults = Indexer.index(parseResults)
        print(crawlResults, parseResults, indexResults)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    DB = DataBase()
    Parser.DB = DB
    main()
    print("Exited at {Time}".format(Time=datetime.now()))
