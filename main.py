import json
import os
import requests
from datetime import datetime, timezone

stored_user_name = ""

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

r_user_data()
print("\nType 'exit' to exit the program & 'help' to see the list of commands.")

while True:
    cmdl = input(f"\n{stored_user_name}@shipwrecked:~/$ ")

    if cmdl == "help":
        print("help - Show this help message")
        print("exit - Exit the program")
        print("whoami - Show your user data")
        print("session - Show your session data")
        print("progress - Show your progress to the island!")
    elif cmdl == "whoami":
        whoami()
    elif cmdl == "session":
        session()
    elif cmdl == "progress":
        progress()
    elif cmdl == "exit":
        print("Until next time!")
        break
