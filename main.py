import json
import os
import requests
from datetime import datetime, timezone

stored_user_name = ""
inShop = False

if not os.path.exists("data.json"):
    print("Welcome to ShipwreckedCLI. Let's get you all setup.")
    print("Well first start by logging you in!")
    print("You will find all the cookies you need for logging in under the 'Application' tab in the 'Cookies' section of your browser.\n")
    csrf_token = input("Please input your csrf-token (__Host-next-auth.csrf-token): ")
    callback_url = input("Please input your callback-url (__Secure-next-auth.callback-url): ")
    session_token = input("Please input your session-token (__Secure-next-auth.session-token): ")

    data = {
        "csrf_token": csrf_token,
        "callback_url": callback_url,
        "session_token": session_token
    }

    with open("data.json", "w") as file:
        file.write(json.dumps(data))
else:
    print("Welcome back!")

with open("data.json", "r") as file:
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
    cmdline = f"\n{stored_user_name}@shipwrecked:~/{currentscreen}$ "
    return cmdline

def whoami():
    tmp_user_data = r_user_data()
    print(f"Name: {tmp_user_data['name']}")
    print(f"Email: {tmp_user_data['email']}")
    print(f"Email Verified: {tmp_user_data['emailVerified']}")
    print(f"Hackatime ID: {tmp_user_data['hackatimeId']}")
    print(f"ID: {tmp_user_data['id']}")
    print(f"Identity Token: {tmp_user_data['identityToken']}")
    print(f"Image: {tmp_user_data['image']}")
    print(f"isAdmin: {tmp_user_data['isAdmin']}")
    print(f"isShopAdmin: {tmp_user_data['isShopAdmin']}")
    print(f"isShopOrdersAdmin: {tmp_user_data['isShopOrdersAdmin']}")
    print(f"Slack: {tmp_user_data['slack']}")
    print(f"Status: {tmp_user_data['status']}")

def session():
    r = requests.get("https://shipwrecked.hackclub.com/api/auth/session", headers=user_headers)
    
    target_time = datetime.fromisoformat(r.json()['expires'])
    current_time = datetime.now(timezone.utc)
    time_diff = target_time - current_time
    days = time_diff.days
    remaining_seconds = time_diff.seconds
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds % 3600) // 60
    seconds = remaining_seconds % 60

    microseconds = time_diff.microseconds
    total_seconds_with_decimal = seconds + microseconds / 1_000_000
    print(f"Session expires in: {days} days, {hours} hours, {minutes} minutes and {total_seconds_with_decimal:.0f} seconds ({target_time})")

def progress():
    r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shells", headers=user_headers)
    data = r.json()

    print(f"Island Progress: {data["progress"]["total"]["percentage"]}% (earned: {data["progress"]["total"]["percentage"] - data["progress"]["purchased"]["percentage"]} | purchased {data["progress"]["purchased"]["percentage"]})")
    print(f"Shells: {data["shells"]} (earned: {data["earnedShells"]} | spent: {data["totalSpent"]})")

def print_shop_submenu_help_screen():
    print("--- Shop Submenu Commands ---")
    print("items - view shop items")
    print("purchase <item> - buy shop item (under construction - not working rn)")
    print("orders - view shop orders")
    print("back - exit back to main programm")

def print_shop_items():
    r = requests.get("https://shipwrecked.hackclub.com/api/bay/shop/items", headers=user_headers)
    r2 = requests.get("https://shipwrecked.hackclub.com/api/users/me/shells", headers=user_headers)
    data = r.json()
    shell_data = r2.json()

    print(f"Shell Shop ({shell_data["shells"]} shells available | {len(data["items"])} in shop)")
    for item in data["items"]:
        print(f"\n- {item["name"]} (id: {item["id"]}) -")
        print(item["description"])
        print(f"Price {item["price"]}")

def print_shop_orders():
    r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shop-orders", headers=user_headers)
    data = r.json()
    data2 = data["orders"]

    status_ff = 0
    status_p = 0
    for order in data2:
        if order["status"] == "fulfilled":
            status_ff += 1
        elif order["status"] == "pending":
            status_p += 1

    print(f"You have {len(data2)} orders ({status_ff} fulfilled | {status_p} pending)")

    for order in data2:
        print(f"\n- {order["itemName"]} (id: {order["itemId"]} | orderID: {order["id"]}) -")
        print(f"Quantity: {order["quantity"]}")
        print(f"Price: {order["price"]} ({order["price"] / order["quantity"]:.0f} per item)")

r_user_data()
print("\nType 'exit' to exit the program & 'help' to see the list of commands.")

while True:
    cmdl = input(generate_cmd_line()).lower()

    if inShop == True:
        if cmdl == "back":
            inShop = False
        elif cmdl == "help":
            print_shop_submenu_help_screen()
        elif cmdl == "items":
            print_shop_items()
        elif cmdl == "orders":
            print_shop_orders()
    elif "help" in cmdl:
        cmdl = cmdl.split(" ")
        if len(cmdl) == 2:
            if "shop" in cmdl[1]:
                print_shop_submenu_help_screen()
        elif len(cmdl) == 1:
            print("--- General commands ---")
            print("help - Show this help message")
            print("whoami - Show your user data")
            print("session - Show your session data")
            print("progress - Show your progress to the island!")
            print("\n--- Submenus (use help <submenu> to view commands help page) ---")
            print("shop - enter the shop")
        else:
            print("Uh oh, seems like that help command was invalid.")
            print(len(cmdl))
        print("exit - Exit the program")
    elif cmdl == "whoami":
        whoami()
    elif cmdl == "session":
        session()
    elif cmdl == "progress":
        progress()
    elif cmdl == "shop":
        inShop = True
    elif cmdl == "exit":
        print("Until next time!")
        break
    else:
        print("Uh oh, seems like you have entered an invalid or unknown command.")
