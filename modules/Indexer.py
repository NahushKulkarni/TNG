def index(parseResult, DB):
    return DB.addToContentRepository(dataDict=parseResult)


def appendURLs(crawlResults, DB):
    try:
        DB.addToURLStore(crawlResults['links'])
        return True
    except Exception as e:
        print(e)
        return False
