from os import times
import yaml
import tkinter
import tkinter.ttk

from parsers.rss10 import RSS10Parser
from parsers.rss20 import RSS20Parser

class Entry:
  def __init__(self, title: str, items: list[dict[str, str]]) -> None:
    self.title = title
    self.items = items

class Application:
  def start(self) -> None:
    self.entries = data = self.getlist()
    window = self.creategui(data)
    window.mainloop()

  def getlist(self) -> list[Entry]:
    result = []
    with open("config.yaml", "r", encoding="utf-8") as f:
      data = yaml.safe_load(f)

      for item in data:
        i = None
        if item["class"] == "RSS10Parser":
          i = RSS10Parser(item["url"]).getlist()
        elif item["class"] == "RSS20Parser":
          i = RSS20Parser(item["url"]).getlist()
        result.append(Entry(item["title"], i))
    return result

  def creategui(self, entries: list[Entry]) -> tkinter.Tk:
    window = tkinter.Tk("Tool")
    note = tkinter.ttk.Notebook(window)
    note.pack(expand=True, fill=tkinter.BOTH)
    for entry in entries:
      content = tkinter.Listbox(note)
      for item in entry.items:
        content.insert(tkinter.END,
        item["title"][len(entry.title):] if item["title"].startswith(entry.title) else item["title"])
      content.pack(expand=True, fill=tkinter.BOTH)
      note.add(content, text=entry.title)
    return window


if __name__ == "__main__":
  Application().start()