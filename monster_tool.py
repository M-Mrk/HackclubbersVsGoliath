from application.db import db, Monsters
from colorama import Fore, Back, Style, init
from app import get_app
import os, sys
import readchar
from datetime import datetime, timezone

init()

def get_all_monsters():
    return db.session.query(Monsters).all()

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def clear_single_line():
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def moveCursorUp(lines=1):
    for x in range(lines):
        sys.stdout.write("\033[f")
    sys.stdout.flush()

def clear_lines(lines):
    for x in range(lines):
        sys.stdout.write("\033[1A")
        sys.stdout.write("\033[K")
    sys.stdout.flush()

class OptionSel:
    def __init__(self, name, returns):
        self.name = name
        self.returns = returns

def selection_menu(options):
    selected = False
    current_hover = 0
    while not selected == True:
        for index, option in enumerate(options):
            if index == current_hover:
                before = "> " + Back.CYAN + Fore.BLACK
            else:
                before = "  " + Back.RESET
            print(before + option.name + Style.RESET_ALL)
        got_input = False
        while not got_input:
            user_input = readchar.readkey()
            if user_input == readchar.key.UP:
                current_hover -= 1
                got_input = True
            elif user_input == readchar.key.DOWN:
                current_hover += 1
                got_input = True
            elif user_input == readchar.key.ENTER or user_input == readchar.key.RIGHT:
                selected = True
                got_input = True
            else:
                continue

            if current_hover > (len(options)-1):
                current_hover = 0
            if current_hover < 0:
                current_hover = (len(options)-1)
            clear_lines(len(options))
    selected_option = options[current_hover]
    return selected_option.returns

class WriteReturn:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def writable_menu(options):
    current_hover = 0
    options.append("Done")
    entries = []
    for option in options:
        entry = WriteReturn(name=option, value="")
        entries.append(entry)
    while True:
        for index, entry in enumerate(entries):
            if index == current_hover:
                before = "> " + Fore.CYAN
            else:
                before = "  "
            if entry.name == "Done":
                print(before + "Done?" + Style.RESET_ALL)
            else:
                value = entry.value
                print(before + entry.name + Style.RESET_ALL + ":" + value)
        
        user_input = readchar.readkey()
        if user_input == readchar.key.UP:
            current_hover -= 1
        elif user_input == readchar.key.DOWN or user_input == readchar.key.ENTER:
            if current_hover == (len(entries) - 1) and user_input == readchar.key.ENTER:
                clear_lines(len(entries))
                return entries[:-1]
            current_hover += 1
        elif user_input == readchar.key.BACKSPACE:
            if len(entries[current_hover].value) > 0:
                entries[current_hover].value = entries[current_hover].value[:-1]
        else:
            entries[current_hover].value += user_input

        if current_hover > (len(options)-1):
            current_hover = 0
        if current_hover < 0:
            current_hover = (len(options)-1)

        clear_lines(len(options))

# DATESPACING = 21
# datespacer = ""
# for x in range((DATESPACING/2)):
#     datespacer += DATESPACING

def show_monsters():
    app = get_app()
    with app.app_context():
        monsters = get_all_monsters()
        print(Fore.CYAN + f"{len(monsters)} Monsters in DB" + Style.RESET_ALL)
        # max_name_length = 0
        # max_url_length = 0
        # for monster in monsters:
        #     name = monster.name
        #     if len(name) > max_name_length:
        #        max_name_length = len(name)
        #     url = monster.url
        #     if len(url) > max_url_length:
        #         max_url_length = len(url)

        # name_space = " "
        # for x in range((max_name_length/2)):
        #     name_space += " "

        # url_space = " "
        # for x in range((max_url_length/2)):
        #     url_space += " "

        # print(f"  Id  |{name_space}Name{name_space}|  health  |  max_health  |{datespacer}created_at{datespacer}|  active  |{datespacer}defeated_at{datespacer}|{url_space}url{url_space}")
        # for monster in monsters:
        #     print(monster.id )
        for monster in monsters:
            print(f"id: {monster.id}, name: {monster.name}, health: {monster.health}, max_health: {monster.max_health}, created_at: {monster.created_at}, active: {monster.active}, defeated_at: {monster.defeated_at}, url: {monster.url}")
        print("WORK IN PROGRESS")
        SHOWMONSTERSOPTIONS = [
            OptionSel("return", "return")
        ]
        selection_menu(SHOWMONSTERSOPTIONS)
        clear_lines(len(monsters)+2)
        return

def add_monster():
    app = get_app()
    with app.app_context():
        monster_attributes = [
            "name",
            "health",
            "attack_power",
            "url"
        ]
        monster_values = writable_menu(monster_attributes)
        print("Adding Monster...")
        try:
            new_monster = Monsters(
                name=monster_values[0].value,
                health=monster_values[1].value,
                max_health=monster_values[1].value,
                attack_power=monster_values[2].value,
                url=monster_values[3].value
            )
            db.session.add(new_monster)
            db.session.commit()
            print(Fore.GREEN + "Monster added successfully!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Could not add Monster, because of: {e}" + Style.RESET_ALL)
            return

def main():
    try:
        print(Fore.CYAN + "Fetching Monsters from DB...")
        try:
            clear()
            app = get_app()
            with app.app_context():
                get_all_monsters()
                
        except Exception as e:
            print(Fore.RED + f"Could not fetch Monsters, because of: {e}")
            print(Fore.RED + "Exiting...")
            return
        
        while True:
            MENUOPTIONS = [
                OptionSel("Show Monsters", "show"),
                OptionSel("Add Monster", "add"),
                OptionSel("Edit Monster", "edit"),
                OptionSel("Quit", "quit")
            ]
            user_decision = selection_menu(MENUOPTIONS)
            if user_decision == "quit":
                print(Fore.YELLOW + "Exiting...")
                return
            elif user_decision == "show":
                show_monsters()
            elif user_decision == "add":
                add_monster()
            elif user_decision == "edit":
                print(Fore.YELLOW + "Edit Monster is not implemented yet." + Style.RESET_ALL)
        
            

    except Exception as e:
        print(Fore.RED + f"Critical Error occured: {e}")
        print(Fore.RED + "Exiting...")

if __name__ == "__main__":
    main()