from typing import Optional
import yaml
import tkinter
import tkinter.ttk
import webbrowser

import pyperclip

from parsers.rss10 import RSS10Parser
from parsers.rss20 import RSS20Parser

class Entry:
  """
  エントリーを示す構造体
  """
  def __init__(self, title: str, items: list[dict[str, str]]) -> None:
    """
    コンストラクタ

    Parameters
    ----
    title: タイトル
    items: エントリー内の項目一覧。title, link, descriptionが格納されている
    """
    self.title = title
    self.items = items

class Application:
  def start(self) -> None:
    """
    プログラムを開始する
    """
    self.listboxes: list[tkinter.Listbox] = []
    self.entries = data = self.getlist()
    self.window = window = self.creategui(data)
    window.mainloop()

  def getlist(self) -> list[Entry]:
    """
    エントリーリストを取得する

    Returns
    ----
    エントリーリスト
    """
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
    """
    GUIを構築する

    Parameters
    ----
    entries: エントリーリスト

    Returns
    ----
    ウィンドウオブジェクト
    """
    window = tkinter.Tk("Tool")
    self.getbuttonbar(window).pack(expand=True, side=tkinter.BOTTOM, fill=tkinter.X)
    self.gettabs(window, entries).pack(expand=True, fill=tkinter.BOTH)
    return window

  def gettabs(self, owner: tkinter.Tk, entries: list[Entry]) -> tkinter.ttk.Notebook:
    """
    タブオブジェクトを生成する

    Parameters
    ----
    owner: オーナーとなるウィンドウオブジェクト
    entries: エントリーリスト

    Returns
    ----
    タブオブジェクト
    """
    note = tkinter.ttk.Notebook(owner)
    for entry in entries:
      content = tkinter.Listbox(note)
      for item in entry.items:
        content.insert(tkinter.END,
        item["title"][len(entry.title):] if item["title"].startswith(entry.title) else item["title"])
      content.pack(expand=True, fill=tkinter.BOTH)
      self.listboxes.append(content)
      note.add(content, text=entry.title)
    return note

  def getbuttonbar(self, owner: tkinter.Frame) -> tkinter.Frame:
    """
    ボタンバーを生成する

    Parameters
    ----
    owner: オーナーとなるウィンドウオブジェクト

    Returns
    ----
    ボタンバー
    """
    frame = tkinter.Frame(owner)
    openbtn = tkinter.Button(frame, text="OPEN", command=self.on_openbtn_click)
    openbtn.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=4, pady=4)
    copyvalues = tkinter.StringVar(frame)
    copyvalues.set("COPY")
    copybtn = tkinter.OptionMenu(frame, copyvalues,
      "Plain", "Markdown", "URL Only", "Plain+", command=self.on_copybtn_click)
    copybtn.pack(fill=tkinter.X, side=tkinter.LEFT, expand=True, padx=4, pady=4)
    return frame

  def on_openbtn_click(self) -> None:
    """
    OPENボタンクリック時の動作
    """
    item = self.getcurrentitem()
    if item is not None:
      webbrowser.open(item["link"])

  def on_copybtn_click(self, selection: str) -> None:
    """
    COPYボタンクリック時の動作

    Parameters
    ----
    selection: 選択したメニュー項目のキャプション
    """
    item = self.getcurrentitem()
    if item is not None:
      text = ""
      if selection == "Plain":
        text = f"{item['title']} {item['link']}"
      elif selection == "Markdown":
        text = f"[{item['title']}]({item['link']})"
      elif selection == "URL Only":
        text = f"{item['link']}"
      elif selection == "Plain+":
        text = f"{item['title']} [{item['link']}]({item['link']})"
      if text != "":
        pyperclip.copy(text)


  def getcurrentitem(self) -> Optional[dict[str, str]]:
    """
    現在の選択中タブのリストで選択中の項目を示す値を取得する

    Returns
    ----
    値。項目が選択されていない場合はNone
    """
    index = self.window.children["!notebook"].index(self.window.children["!notebook"].select())
    return self.entries[index].items[self.listboxes[index].curselection()[0]] \
      if len(self.listboxes[index].curselection()) == 1 else None

if __name__ == "__main__":
  Application().start()