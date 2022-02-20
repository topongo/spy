import curses
import json
from random import choice, shuffle
from time import sleep


places = json.load(open("luoghi.json"))

def main_local(scr, luogo):
  spy = choice(gente)
  for i in gente:
    scr.clear()
    scr.addstr(0, 0, f"passa il telefono a {i}, {i} premi invio.")
    while scr.getch() != ord("\n"):
       pass
    scr.clear()
    scr.addstr(0, 0, "sei la spia" if spy == i else f"siamo in {luogo}")
    scr.addstr(1, 0, "quando hai letto premi invio")
    while scr.getch() != ord("\n"):
      pass
  scr.clear()
  scr.getch()
  with open("spy", "w+") as s:
    s.write(spy)
  curses.napms(1000*60*6)
  return spy


def main_telegram(luogo, master):
  spy = choice(gente)

  # wait for responses

with open("people") as p:
  gente = p.read().split()
shuffle(gente)
place = choice(places, )
if len(argv) > 1 and argv[1] == "telegram":
  main_telegram(place)
else:
  print(curses.wrapper(main, place))
