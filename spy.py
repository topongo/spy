import curses
import json
from random import choice, shuffle, randint
from os.path import exists
from sys import argv
from time import sleep


def main_local(place):
    if not exists("people"):
        with open("people", "w+"):
            pass

    with open("people") as p:
        people = p.read().split()
        if len(people) == 0:
            print("no people provided")
            exit()

    def assign(scr):
        spy = choice(people)
        for i in people:
            scr.clear()
            scr.addstr(0, 0, f"passa il telefono a {i}, {i} premi invio.")
            while scr.getch() != ord("\n"):
                pass
            scr.clear()
            scr.addstr(0, 0, "sei la spia" if spy == i else f"siamo in {place}")
            scr.addstr(1, 0, "quando hai letto premi invio")
            while scr.getch() != ord("\n"):
                pass
        scr.clear()
        scr.getch()
        with open("spy", "w+") as s:
            s.write(spy)
        curses.napms(1000 * 60 * 6)
        return spy

    print(curses.wrapper(assign))


def main_telegram(place):
    from telebotapi import TelegramBot

    def objectify(id_):
        return TelegramBot.Chat({"id": id_})

    print("Starting bot...", end="")
    t = TelegramBot("5105835451:AAGAOK0l9CZ_PFbfisEVxKKi-t34Vw-Bexk")
    t.bootstrap()
    print(" Done")
    pin = randint(1000, 9999)
    print(f"PIN: {pin}")

    stop = False
    people = {}
    master = 0
    # wait for pin
    while not stop:
        for i in t.get_updates():
            try:
                c = i.content.chat
                text = i.content.text
            except AttributeError:
                continue
            try:
                if int(text) == pin:
                    master = c.id
                    people[master] = c.username
                    t.sendMessage(c, "Sei il master ora. E sei anche iscritto.")
                    print(f"Master is {people[master]}")
                    stop = True
            except ValueError:
                pass

    stop = False
    print("Waiting for enrollments")
    # wait for responses
    while not stop:
        for i in t.get_updates():
            try:
                c = i.content.chat
                text = i.content.text
            except AttributeError:
                continue
            if text == "CLOSE":
                master = c.id
                stop = True
            elif c.id not in people:
                people[c.id] = c.username
                t.sendMessage(objectify(c.id), f"Iscritto, apsetta che il master chiuda le iscrizioni. (Invia \"EXIT\" "
                                               f"per disiscriverti)")
            elif text == "EXIT":
                if c.id == master:
                    t.sendMessage(objectify(c.id), f"Sei il master, non puoi disiscriverti")
                else:
                    people.pop(c.id)
                    t.sendMessage(objectify(c.id), f"Disiscritto. Invia un altro messaggio per reiscriverti.")
            print(f"People: {', '.join(people.values())}")
        sleep(.5)

    if len(people) == 0:
        t.sendMessage(objectify(master), "Not enough people for playing.")
        return
    else:
        spy = choice(list(people.keys()))
        p_list = list(people.items())
        shuffle(p_list)
        print(p_list)
        people = dict(p_list)

    for i in people:
        if i == spy:
            t.sendMessage(objectify(i), "Sei la spia.")
        else:
            t.sendMessage(objectify(i), f"Siamo in {place}")

    stop = False
    while not stop:
        for i in t.get_updates():
            print(i)
            try:
                c = i.content.chat
                text = i.content.text
            except AttributeError:
                continue
            if c.id == master and text == "END":
                for j in people:
                    t.sendMessage(objectify(j), f"La spia era [@{people[spy]}](tg://user?id={spy})")
                stop = True
                sleep(5)
        sleep(.5)


places = json.load(open("luoghi.json"))

place_ = choice(places)
if len(argv) > 1 and argv[1] == "telegram":
    main_telegram(place_)
else:
    main_local(place_)
