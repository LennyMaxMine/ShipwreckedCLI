import json
import os
import requests
from datetime import datetime, timezone

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

from src.leaderboard import LeaderboardOriginal
from src.fetch import FetchClassOriginal
from src.whoami import WhoamiClassOriginal
from src.session import SessionClassOriginal
from src.progress import ProgressClassOriginal

from src.submenus.gallery import GalleryClassOriginal
from src.submenus.projects import ProjectsClassOriginal
from src.submenus.user import UserClassOriginal
from src.submenus.shop import ShopClassOriginal

version = "1.0.0"

configfilepath = "iljhna.shipwreckedcli"

stored_user_name = ""
inShop = False
inUser = False
inProjects = False
inGallery = False

if not os.path.exists(configfilepath):
    print("Welcome to ShipwreckedCLI. Let's get you all setup.")
    print("Well first start by logging you in!")
    print("You will find all the cookies you need for logging in under the 'Application' tab in the 'Cookies' section of your browser.\n")
    csrf_token = input("Please input your csrf-token (__Host-next-auth.csrf-token): ")
    callback_url = "https%3A%2F%2Fshipwrecked.hackclub.com%2Fbay" #input("Please input your callback-url (__Secure-next-auth.callback-url): ")
    session_token = input("Please input your session-token (__Secure-next-auth.session-token): ")

    data = {
        "csrf_token": csrf_token,
        "callback_url": callback_url,
        "session_token": session_token
    }

    with open(configfilepath, "w") as file:
        file.write(json.dumps(data))
else:
    print("Welcome back!")

with open(configfilepath, "r") as file:
    user_data = json.load(file)
    
    user_headers = {
        "Cookie": f"__Host-next-auth.csrf-token={user_data['csrf_token']}; __Secure-next-auth.callback-url={user_data['callback_url']}; __Secure-next-auth.session-token={user_data['session_token']}"
    }

def r_user_data():
    r = requests.get("https://shipwrecked.hackclub.com/api/users/me", headers=user_headers)
    global stored_user_name
    stored_user_name = r.json()['name'].lower()
    return r.json()

def generate_cmd_line():
    currentscreen = ""
    if inShop == True:
        currentscreen = "shop/"
    elif inUser == True:
        currentscreen = "user/"
    elif inProjects == True:
        currentscreen = "projects/"
    elif inGallery == True:
        currentscreen = "gallery/"
    cmdline = f"\n{stored_user_name}@shipwrecked:~/{currentscreen}$ "
    return cmdline

def cmdl_exit():
    print("Until next time!")
    exit()

def cmdl_cmd_not_found():
    print("Uh oh, seems like you have entered an invalid or unknown command.")

def cmdl_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_submenu_help_screen():
    print("\n--- Submenus (use help <submenu> to view commands help page) ---")
    print("Use cd <submenu> to enter a submenu")
    print("shop - enter the shop")
    print("user - enter the shipwrecked settings screen")
    print("projects - enter the projects submenu")
    print("gallery - enter the gallery submenu")

def disableallSubmenu():
    global inShop, inUser, inProjects, inGallery
    inShop = False
    inUser = False
    inProjects = False
    inGallery = False

r_user_data()

gallery_class = GalleryClassOriginal()
gallery_class.set_user_hdr(user_headers)

projects_class = ProjectsClassOriginal()
projects_class.set_user_hdr(user_headers)

leaderboard_class = LeaderboardOriginal()
leaderboard_class.set_user_hdr(user_headers)

user_class = UserClassOriginal()
user_class.set_user_hdr(user_headers)

shop_class = ShopClassOriginal()
shop_class.set_user_hdr(user_headers)

fetch_class = FetchClassOriginal()
fetch_class.set_user_hdr(user_headers)
fetch_class.set_ver(version)

whoami_class = WhoamiClassOriginal()

session_class = SessionClassOriginal()
session_class.set_user_hdr(user_headers)

progress_class = ProgressClassOriginal()
progress_class.set_user_hdr(user_headers)


print("\nType 'exit' to exit the program & 'help' to see the list of commands.")

main_commands = [
    'exit', 'clear', 'cd', 'help', 'ls', 'whoami', 'session', 'progress', 'leaderboard', 'fetch', 'logout'
]
shop_commands = ['items', 'purchase', 'orders', 'inventory', 'back', 'cd ..', 'help']
user_commands = ['name', 'email', 'address', 'birthday', 'phone', 'id', 'email-verification', 'identity-verification', 'slack-connected', 'back', 'cd ..', 'help']
projects_commands = ['list', 'details', 'reviews', 'stats', 'back', 'cd ..', 'help']
gallery_commands = ['list', 'details', 'upvote', 'popular', 'recent', 'search', 'stats', 'back', 'cd ..', 'help']

all_submenus = ['shop', 'user', 'projects', 'gallery']

class CommandAutoSuggest(AutoSuggest):
    def get_suggestion(self, buffer, document):
        text = document.text_before_cursor
        if inShop:
            options = shop_commands
        elif inUser:
            options = user_commands
        elif inProjects:
            options = projects_commands
        elif inGallery:
            options = gallery_commands
        else:
            options = main_commands + [f'cd {submenu}' for submenu in all_submenus]
        matches = [cmd for cmd in options if cmd.startswith(text) and cmd != text]
        if matches:
            suggestion = matches[0][len(text):]
            return Suggestion(suggestion)
        return None

while True:
    if inShop:
        completer = WordCompleter(shop_commands, ignore_case=True)
    elif inUser:
        completer = WordCompleter(user_commands, ignore_case=True)
    elif inProjects:
        completer = WordCompleter(projects_commands, ignore_case=True)
    elif inGallery:
        completer = WordCompleter(gallery_commands, ignore_case=True)
    else:
        completer = WordCompleter(main_commands + [f'cd {submenu}' for submenu in all_submenus], ignore_case=True)
    cmdl = prompt(generate_cmd_line(), completer=completer, auto_suggest=CommandAutoSuggest())
    cmdl = cmdl.lower()

    if cmdl == "exit":
        cmdl_exit()
    elif cmdl == "clear":
        cmdl_clear()
    elif cmdl == "cd ..":
        disableallSubmenu()
    elif inShop == True:
        if cmdl == "back":
            inShop = False
        elif cmdl.startswith("help"):
            shop_class.print_shop_submenu_help_screen()
        elif cmdl == "items":
            shop_class.print_shop_items()
        elif cmdl == "orders":
            shop_class.print_shop_orders()
        elif cmdl == "inventory":
            shop_class.print_shop_inventory()
        else:
            cmdl_cmd_not_found()
    elif inUser == True:
        if cmdl.startswith("help"):
            user_class.print_user_submenu_help_screen()
        elif cmdl == "back":
            inUser = False
        elif cmdl == "exit":
            cmdl_exit()
        else:
            user_class.user_submenu_commands(cmdl)
    elif inProjects == True:
        if cmdl.startswith("help"):
            projects_class.print_projects_submenu_help_screen()
        elif cmdl == "back":
            inProjects = False
        elif cmdl == "list":
            projects_class.print_projects_list()
        elif cmdl == "stats":
            projects_class.print_project_stats()
        elif cmdl.startswith("details"):
            cmdl_parts = cmdl.split(" ")
            if len(cmdl_parts) == 2:
                projects_class.print_project_details(cmdl_parts[1])
            else:
                print("Usage: details <project_id>")
        elif cmdl.startswith("reviews"):
            cmdl_parts = cmdl.split(" ")
            if len(cmdl_parts) == 2:
                projects_class.print_project_reviews(cmdl_parts[1])
            else:
                print("Usage: reviews <project_id>")
        else:
            cmdl_cmd_not_found()
    elif inGallery == True:
        if cmdl.startswith("back"):
            inGallery = False
        elif cmdl.startswith("help"):
            gallery_class.print_gallery_submenu_help_screen()
        elif cmdl.startswith("list"):
            parts = cmdl.split()
            if len(parts) == 2 and parts[1].isdigit():
                gallery_class.print_gallery_list(int(parts[1]))
            else:
                gallery_class.print_gallery_list()
        elif cmdl.startswith("details"):
            cmdl_parts = cmdl.split(" ")
            if len(cmdl_parts) == 2:
                gallery_class.print_gallery_project_details(cmdl_parts[1])
            else:
                cmdl_cmd_not_found()
        elif cmdl == "popular":
            gallery_class.print_gallery_popular()
        elif cmdl == "recent":
            gallery_class.print_gallery_recent()
        elif cmdl == "stats":
            gallery_class.print_gallery_stats()
        elif cmdl.startswith("search"):
            cmdl_parts = cmdl.split(" ", 1)
            if len(cmdl_parts) == 2:
                gallery_class.search_gallery(cmdl_parts[1])
            else:
                cmdl_cmd_not_found()
        elif cmdl.startswith("upvote"):
            cmdl_parts = cmdl.split(" ")
            if len(cmdl_parts) == 2:
                gallery_class.upvote_project(cmdl_parts[1])
            else:
                cmdl_cmd_not_found()
        else:
            cmdl_cmd_not_found()
    elif "help" in cmdl:
        cmdl = cmdl.split(" ")
        if len(cmdl) == 2:
            if "shop" in cmdl[1]:
                shop_class.print_shop_submenu_help_screen()
            elif "user" in cmdl[1]:
                user_class.print_user_submenu_help_screen()
            elif "projects" in cmdl[1]:
                projects_class.print_projects_submenu_help_screen()
            elif "gallery" in cmdl[1]:
                gallery_class.print_gallery_submenu_help_screen()
        elif len(cmdl) == 1:
            print("--- General commands ---")
            print("help - Show this help message")
            print("ls - Show all submenus")
            print("whoami - Show your user data")
            print("session - Show your session data")
            print("progress - Show your progress to the island!")
            print("leaderboard <length> - Show the leaderboard sorted by hours")
            print("fetch - Fetch your ShipwreckedCli information")
            print("logout - Delete all locally stored data")
            print_submenu_help_screen()
        else:
            print("Uh oh, seems like that help command was invalid.")
            print(len(cmdl))
        print("\n --- Always available commands ---")
        print("clear - Clear the screen")
        print("exit - Exit the program")
    elif cmdl == "whoami":
        whoami_class.whoami(r_user_data())
    elif cmdl == "session":
        session_class.session()
    elif cmdl == "progress":
        progress_class.progress()
    elif cmdl.startswith("cd"):
        cmdl = cmdl.split()
        if len(cmdl) == 2:
            if cmdl[1] == "shop":
                inShop = True
            elif cmdl[1] == "user":
                inUser = True
            elif cmdl[1] == "projects":
                inProjects = True
            elif cmdl[1] == "gallery":
                inGallery = True
            else:
                cmdl_cmd_not_found()
        else:
            cmdl_cmd_not_found()
    elif cmdl.startswith("leaderboard"):
        cmdl = cmdl.split()
        try:
            if len(cmdl) == 2:
                tmp = int(cmdl[1])
            elif len(cmdl) == 1:
                tmp = 10
            else:
                cmdl_cmd_not_found()
                continue
            leaderboard_class.leaderboard(stored_user_name, tmp)
        except:
            cmdl_cmd_not_found()
    elif cmdl == "fetch":
        fetch_class.fetch(r_user_data())
    elif cmdl == "logout":
        if (input("Are you sure you want to logout? (this cant be undone) (y/n): ")).lower() == "y":
            os.remove(configfilepath)
            cmdl_exit()
    elif cmdl == "ls":
        print_submenu_help_screen()
    else:
        cmdl_cmd_not_found()