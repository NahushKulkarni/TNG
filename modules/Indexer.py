def index(parseResult, URL, DB):
    return DB.addToContentRepository([URL], [parseResult])


def appendURLs(crawlURL, crawlResults, DB):
    try:
        DB.deleteFromURLStore(DB.getURLID(crawlURL))
        DB.addToURLStore(crawlResults['links'])
        return True
    except Exception as e:
        print(e)
        return False
