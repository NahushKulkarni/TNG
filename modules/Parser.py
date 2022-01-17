ExclusionTable = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make",
                  "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"]

TopLevelThreshold = 50


def parse(crawlResults):
    textualData = crawlResults['headings'] + crawlResults['text']

    pageDiscription = ""
    if len(crawlResults['meta']) > 0:
        pageDiscription = crawlResults['meta'][0]

    mediaData = crawlResults['images'] + \
        crawlResults['videos'] + crawlResults['audios'] + \
        crawlResults['documents']

    textOccurance = OccuranceTable(textualData)

    for ET in ExclusionTable:
        if ET in textOccurance:
            textOccurance.pop(ET)

    textOccurance = sorted(textOccurance.items(),
                           key=lambda x: x[1], reverse=True)
    textOccurance = textOccurance[:TopLevelThreshold]

    return {'Description': pageDiscription, 'pageTitle': crawlResults['title'], 'OccuranceTable': textOccurance, 'MediaURLs': mediaData, 'ContactURLs': crawlResults['contacts']}


def OccuranceTable(textualData):
    Occurance = {}
    for entry in textualData:
        entry = entry.lower()
        for word in entry.split():
            if word in Occurance:
                Occurance[word] += 1
            else:
                Occurance[word] = 1
    return Occurance
