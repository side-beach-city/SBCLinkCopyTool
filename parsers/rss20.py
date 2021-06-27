import urllib.request
import xml.etree.ElementTree

class RSS20Parser:
  def __init__(self, url: str) -> None:
    self.url = url

  def getlist(self) -> list[dict[str, str]]:
    result = []
    with urllib.request.urlopen(self.url) as res:
      data = xml.etree.ElementTree.fromstring(res.read())
      for child in data[0].iter("item"):
        result.append({
          "title": child.find("title").text,
          "link": child.find("link").text,
          "description": child.find("description").text,
        })
    return result

if __name__ == "__main__":
  import pprint
  pprint.pprint(RSS20Parser("https://sbc.yokohama/feed/podcast").getlist())