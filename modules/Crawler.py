import re
import urllib.request


def crawl(url):
    html = openURL(url)
    if html is None:
        return None
    else:
        links = getLinks(html)
        meta = getMeta(html)
        images = getImages(html)
        videos = getVideos(html)
        headings = removeTags(getHeadings(html))
        text = removeTags(getText(html))
        return {'links': links, 'meta': meta, 'images': images, 'videos': videos, 'headings': headings, 'text': text}


def openURL(url):
    try:
        response = urllib.request.urlopen(url)
        html = response.read()
        return html
    except:
        return None


def getLinks(html):
    links = re.findall(r'href="(.*?)"', str(html))
    return links


def getMeta(html):
    meta = re.findall(r'<meta name="description" content="(.*?)"', str(html))
    return meta


def getImages(html):
    images = re.findall(r'<img src="(.*?)"', str(html))
    return images


def getVideos(html):
    videos = re.findall(r'src="(.*?)"', str(html))
    return videos


def getHeadings(html):
    headings = re.findall(r'<h[1-6]>(.*?)</h[1-6]>', str(html))
    return headings


def getText(html):
    text = re.findall(r'<p>(.*?)</p>', str(html))
    return text


def removeTags(text):
    for i in range(len(text)):
        try:
            text[i] = re.sub(r'<.*?>', '', text[i])
        except:
            continue
    return text


def convertEntities(text):
    for i in range(len(text)):
        try:
            text[i] = re.sub(
                r'&#(\d+);', lambda x: chr(int(x.group(1))), text[i])
        except:
            continue
    return text


def convertEscapeSequences(text):
    for i in range(len(text)):
        try:
            text[i] = re.sub(
                r'\\x(\w+)', lambda x: chr(int(x.group(1), 16)), text[i])
        except:
            continue
    return text
