import re
import urllib.request
from tqdm import tqdm

validRefs = ['/', '//']
validProts = ['https://']
validSubDomains = ['www.', 'm.']
validComms = ['mailto:', 'tel:', 'skype:',
              'whatsapp:', 'telegram:', 'sms:']
validImages = ['jpg', 'png', 'jpeg', 'gif', 'svg', 'webp', 'bmp', 'tiff', 'ico',
               'tif', 'tiff', 'jfif', 'jpe', 'jfif-tbnl', 'jxr', 'pjpeg', 'pjp', 'bpg']
validVideos = ['mp4', 'mov', 'wmv', 'avi', 'flv', 'swf', 'mkv', 'webm']


def crawl(url):
    if not url.startswith('https://'):
        return None
    html = openURL(url)
    if html is None:
        return None
    else:
        try:
            links = getLinksFromSitemap(url) + getLinks(html)
            links, contacts, documents = refineLinks(url, links)
            meta = getMeta(html)
            title = getTitle(html)
            images = convertRelativeLinks(getImages(html), url)
            videos = convertRelativeLinks(getVideos(html), url)
            videos, images = moveToImages(videos, images)
            audios = convertRelativeLinks(getAudios(html), url)
            headings = removeTags(getHeadings(html))
            text = removeTags(getText(html))
            return {'links': links, 'meta': meta, 'title': title, 'documents': documents, 'contacts': contacts, 'images': images, 'videos': videos, 'audios': audios, 'headings': headings, 'text': text}
        except Exception as e:
            print(e)
            return None


def openURL(url):
    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
            }
        )
        response = urllib.request.urlopen(req)
        html = response.read()
        return html
    except:
        return None


def getDomain(url):
    try:
        domain = re.findall(r'(https://.*?)/', url)[0]
        return domain
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


def getAudios(text):
    audios = re.findall(r'(http.*?\.(mp3|ogg|wav))', str(text))
    return audios


def getHeadings(html):
    headings = re.findall(r'<h[1-6]>(.*?)</h[1-6]>', str(html))
    return headings


def getText(html):
    text = re.findall(r'<p>(.*?)</p>', str(html))
    return text


def removeTags(text):
    try:
        for i in range(len(text)):
            try:
                text[i] = re.sub(r'<.*?>', '', text[i])
            except:
                continue
    finally:
        return text


def convertEscapeSequences(text):
    try:
        for i in range(len(text)):
            try:
                text[i] = re.sub(
                    r'\\x(\w+)', lambda x: chr(int(x.group(1), 16)), text[i])
            except:
                continue
    finally:
        return text


def getLinksFromSitemap(url):
    url = getDomain(url)
    sitemap = openURL(url + '/sitemap.xml')
    if sitemap is None:
        return []
    else:
        links = re.findall(r'<loc>(.*?)</loc>', str(sitemap))
        return links


def getTitle(html):
    title = re.findall(r'<title>(.*?)</title>', str(html))
    return title


def moveToImages(videos, images):
    try:
        videos_new = []
        for video in videos:
            extension = video.split('.')[-1].lower()
            if extension in validVideos:
                videos_new.append(video)
            elif extension in validImages:
                images.append(video)
    finally:
        return videos_new, images


def convertRelativeLinks(links, url):
    try:
        domain = getDomain(url)
        for i in range(len(links)):
            if links[i].startswith('/'):
                links[i] = domain + links[i]
            elif links[i].startswith('www.'):
                links[i] = 'https://' + links[i]
    finally:
        return links


def refineLinks(url, links):
    validStarts = validRefs + validProts + validSubDomains + validComms
    contacts = []
    documents = []
    domain = getDomain(url)
    try:
        MaxLimit = len(links)
        for i in range(MaxLimit):
            valid = False

            for start in validStarts:
                if links[i].startswith(start):
                    valid = True
                    break
                elif len(links[i].split('.', 1)[0]) < 8:
                    valid = True
                    break

            if valid:
                if re.search('#', links[i]) or re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', links[i]):
                    valid = False
                elif re.search('mailto:', links[i]) or re.search('tel:', links[i]) or re.search('skype:', links[i]) or re.search('whatsapp:', links[i]) or re.search('telegram:', links[i]) or re.search('sms:', links[i]):
                    contacts.append(links[i])
                    valid = False
                elif links[i].endswith('.pdf') or links[i].endswith('.doc') or links[i].endswith('.docx') or links[i].endswith('.ppt') or links[i].endswith('.pptx') or links[i].endswith('.xls') or links[i].endswith('.xlsx') or links[i].endswith('.txt'):
                    documents.append(links[i])
                    valid = False

            if valid:
                if links[i].startswith('//'):
                    links[i] = 'https:' + links[i]
                elif links[i].startswith('/'):
                    links[i] = domain + links[i]
                elif links[i].startswith('www.') or links[i].startswith('m.'):
                    links[i] = 'https://' + links[i]

            if valid == False:
                links[i] = None

    except Exception as e:
        print("Refining Error: " + str(e))

    finally:
        links = list(set(filter(None, links)))
        contacts = list(set(filter(None, contacts)))
        documents = list(set(filter(None, documents)))
        return links, contacts, documents
