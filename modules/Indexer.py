def index(parseResult, URL, DB):
    return DB.addToContentRepository(dataDict=parseResult)


def appendURLs(crawlURL, crawlResults, DB):
    try:
        DB.addToURLStore(crawlResults['links'])
        return True
    except Exception as e:
        print(e)
        return False
