from os import times
import yaml
import tkinter
import tkinter.ttk
import tkinter.simpledialog

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
    self.getbuttonbar(window).pack(expand=True, side=tkinter.BOTTOM, fill=tkinter.X)
    self.gettabs(window, entries).pack(expand=True, fill=tkinter.BOTH)
    return window

  def gettabs(self, owner: tkinter.Tk, entries: list[Entry]) -> tkinter.ttk.Notebook:
    note = tkinter.ttk.Notebook(owner)
    for entry in entries:
      content = tkinter.Listbox(note)
      for item in entry.items:
        content.insert(tkinter.END,
        item["title"][len(entry.title):] if item["title"].startswith(entry.title) else item["title"])
      content.pack(expand=True, fill=tkinter.BOTH)
      note.add(content, text=entry.title)
    return note

  def getbuttonbar(self, owner: tkinter.Frame) -> tkinter.Frame:
    frame = tkinter.Frame(owner)
    openbtn = tkinter.Button(frame, text="OPEN")
    openbtn.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=4, pady=4)
    copyvalues = tkinter.StringVar(frame)
    copyvalues.set("COPY")
    copybtn = tkinter.OptionMenu(frame, copyvalues,
      "Plain", "Markdown", "URL", "Markdown+")
    copybtn.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=4, pady=4)
    return frame

if __name__ == "__main__":
  Application().start()