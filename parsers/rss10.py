import urllib.request
import xml.etree.ElementTree

class RSS10Parser:
  def __init__(self, url: str) -> None:
    self.url = url

  def getlist(self) -> list[dict[str, str]]:
    ENTRY = r"{http://www.w3.org/2005/Atom}"
    MEDIA = r"{http://search.yahoo.com/mrss/}"
    YOUTUBE = r"{http://www.youtube.com/xml/schemas/2015}"
    result = []
    with urllib.request.urlopen(self.url) as res:
      data = xml.etree.ElementTree.fromstring(res.read())
      for child in data.iter(f"{ENTRY}entry"):
        result.append({
          "title": child.find(f"{ENTRY}title").text,
          "link": child.find(f"{ENTRY}link").attrib["href"],
          "description": child.find(f"{MEDIA}group").find(f"{MEDIA}description").text,
        })
    return result

if __name__ == "__main__":
  import pprint
  pprint.pprint(RSS10Parser("https://www.youtube.com/feeds/videos.xml?playlist_id=PLrPVslFukDQo7l5RCqAZtKDl6tUyMAFWH").getlist())