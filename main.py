import json
import os
from unittest import skip
import requests
from datetime import datetime, timezone
from src import leaderboard
from src.leaderboard import generate_leaderboard, print_leaderboard_table

version = "0.5.0"

configfilepath = "iljhna.shipwreckedcli"

stored_user_name = ""
inShop = False
inUser = False
inProjects = False

if not os.path.exists(configfilepath):
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
    cmdline = f"\n{stored_user_name}@shipwrecked:~/{currentscreen}$ "
    return cmdline

def cmdl_exit():
    print("Until next time!")
    exit()

def cmdl_cmd_not_found():
    print("Uh oh, seems like you have entered an invalid or unknown command.")

def cmdl_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    print("inventory - view your fulfilled orders")
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

def print_shop_inventory():
    r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shop-orders", headers=user_headers)
    data = r.json()
    data2 = data["orders"]

    status_ff = 0
    for order in data2:
        if order["status"] == "fulfilled":
            status_ff += 1

    print(f"You have {status_ff} individual item(s) in your inventory")

    for order in data2:
        if order["status"] == "fulfilled":
            print(f"\n- {order["itemName"]} (id: {order["itemId"]} | orderID: {order["id"]}) -")
            print(f"Quantity: {order["quantity"]} in Inventory")
            print(f"Price: {order["price"]} ({order["price"] / order["quantity"]:.0f} per item)")

def print_user_submenu_help_screen():
    print("--- User Submenu Commands ---")
    print("name - Show your name")
    print("email - Show your email")
    print("address - Show your address")
    print("birthday - Show your birthday")
    print("phone - Show your phone number")
    print("id - print your id")
    print("email-verification - Show your email verification status")
    print("identity-verification - Show your identity verification status")
    print("slack-connected - Show your slack connection status")
    print("back - exit back to main programm")

def user_submenu_commands(field):
    r = requests.get("https://shipwrecked.hackclub.com/api/identity/me", headers=user_headers)
    user_data = r.json()

    try:
        if field == "address":
            for addr in user_data["addresses"]:
                if addr["primary"]:
                    print(f"{addr['line_1']}, {addr['city']}, {addr['state']} {addr['postal_code']}, {addr['country']}")
        elif field == "birthday":
            print(user_data["birthday"])
        elif field == "name":
            print(f"{user_data['first_name']} {user_data['last_name']}")
        elif field == "email":
            print(user_data["primary_email"])
        elif field == "phone":
            print(user_data["phone_number"])
        elif field == "id":
            print(user_data["id"])
        elif field == "email-verification":
            print(user_data["verification_status"])
        elif field == "identity-verification":
            print(user_data["ysws_eligible"])
        elif field == "slack-connected":
            if user_data["slack_id"] is not None or "":
                print(user_data["slack_id"])
            else:
                print("False")
        else:
            print(f"Field '{field}' not found or not supported")
    except:
        cmdl_cmd_not_found()

def leaderboard(top: int):
    r = requests.get("https://shipwrecked.hackclub.com/api/users")
    print("Stored: "+ stored_user_name)
    generate_leaderboard(r.json(), top_n=top, highlight_name=stored_user_name)

def fetch():
    user_data = r_user_data()
        
    progress_r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shells", headers=user_headers)
    progress_data = progress_r.json()
        
    session_r = requests.get("https://shipwrecked.hackclub.com/api/auth/session", headers=user_headers)
    session_data = session_r.json()
        
    target_time = datetime.fromisoformat(session_data['expires'])
    current_time = datetime.now(timezone.utc)
    time_diff = target_time - current_time
    days = time_diff.days
    hours = time_diff.seconds // 3600
        
    orders_r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shop-orders", headers=user_headers)
    orders_data = orders_r.json()
    total_orders = len(orders_data["orders"])
    fulfilled_orders = sum(1 for order in orders_data["orders"] if order["status"] == "fulfilled")
        
    ascii_art = """
         🏴‍☠️ SHIPWRECKED CLI v""" + version + """ 🏴‍☠️
    ⚓ ═══════════════════════════════ ⚓
       🏝️  Welcome aboard, sailor!  🏝️
    """
        
    print(ascii_art)
    print(f"    👤 User: {user_data['name']}")
    print(f"    📧 Email: {user_data['email']}")
    print(f"    🆔 ID: {user_data['id']}")
    print(f"    🐚 Shells: {progress_data['shells']} (earned: {progress_data['earnedShells']}, spent: {progress_data['totalSpent']})")
    print(f"    🏝️ Progress: {progress_data['progress']['total']['percentage']:.1f}%")
    print(f"    📦 Orders: {total_orders} total ({fulfilled_orders} fulfilled)")
    print(f"    ⏰ Session: {days}d {hours}h remaining")
    print(f"    👑 Admin: {'Yes' if user_data.get('isAdmin', False) else 'No'}")
    print(f"    🛒 Shop Admin: {'Yes' if user_data.get('isShopAdmin', False) else 'No'}")
    print(f"    💬 Slack: {'Connected' if user_data.get('slack') else 'Not connected'}")
    print(f"    ✅ Verified: {'Yes' if user_data.get('emailVerified', False) else 'No'}")
    print()
    print("    ⚓ ═══════════════════════════════ ⚓")
    print("      Developed with ♥ by LennyMaxMine")
    print("    Frankfurt, Germany | HC Shipwrecked 2025")
    print("    ⚓ ═══════════════════════════════ ⚓")
    print()
    
def print_projects_submenu_help_screen():
    print("--- Projects Submenu Commands ---")
    print("list - View all your projects")
    print("details <project_id> - View detailed project information")
    print("reviews <project_id> - View project reviews")
    print("stats - Show project statistics")
    print("back - exit back to main program")

def print_projects_submenu_help_screen():
    print("--- Projects Submenu Commands ---")
    print("list - View all your projects")
    print("details <project_id> - View detailed project information")
    print("reviews <project_id> - View project reviews")
    print("stats - Show project statistics")
    print("back - exit back to main program")

def print_projects_list():
    r = requests.get("https://shipwrecked.hackclub.com/api/projects", headers=user_headers)
    data = r.json()
    
    if not data:
        print("You have no projects yet!")
        return
    
    print(f"Your Projects ({len(data)} total)")
    print("=" * 50)
    
    for project in data:
        status_icons = []
        if project["shipped"]: status_icons.append("Shipped")
        if project["submitted"]: status_icons.append("Submitted")
        if project["viral"]: status_icons.append("Viral")
        if project["in_review"]: status_icons.append("In Review")
        
        status_text = " | ".join(status_icons) if status_icons else "Draft"
        
        print(f"\n--- {project['name']} (id: {project['projectID']}) ---")
        print(f"{project['description']}")
        print(f"Status: {status_text} with {project.get('rawHours', 0):.1f}h")
        if project.get('codeUrl'):
            print(f"Code: {project['codeUrl']}")
        if project.get('playableUrl'):
            print(f"Demo: {project['playableUrl']}")

def print_project_details(project_id):
    r = requests.get("https://shipwrecked.hackclub.com/api/projects", headers=user_headers)
    projects = r.json()
    
    project = next((p for p in projects if p['projectID'] == project_id), None)
    
    if not project:
        print(f"Project with ID '{project_id}' not found!")
        return
    
    print(f"Project Details: {project['name']}")
    print("=" * 60)
    print(f"ID: {project['projectID']}")
    print(f"Description: {project['description']}")
    print(f"Total Hours: {project.get('rawHours', 0):.2f}h")

    print(f"\nStatus:")
    print(f"Shipped: {'Yes' if project['shipped'] else 'No'}")
    print(f"Submitted: {'Yes' if project['submitted'] else 'No'}")
    print(f"Viral: {'Yes' if project['viral'] else 'No'}")
    print(f"In Review: {'Yes' if project['in_review'] else 'No'}")
    print(f"Chat Enabled: {'Yes' if project['chat_enabled'] else 'No'}")
    print(f"Has Repo Badge: {'Yes' if project['hasRepoBadge'] else 'No'}")

    print(f"\nLinks:")
    if project.get('codeUrl'):
        print(f"Code: {project['codeUrl']}")
    if project.get('playableUrl'):
        print(f"Demo: {project['playableUrl']}")
    if project.get('screenshot'):
        print(f"Screenshot: {project['screenshot']}")
  
    if project.get('hackatimeLinks'):
        print(f"\nHackatime Breakdown:")
        for link in project['hackatimeLinks']:
            print(f"• {link['hackatimeName']}: {link['hoursOverride']:.2f}h")

def print_project_reviews(project_id):
    r = requests.get(f"https://shipwrecked.hackclub.com/api/reviews?projectId={project_id}", headers=user_headers)
    
    if r.status_code != 200:
        print(f"Error fetching reviews for project {project_id}")
        return
    
    reviews = r.json()
    
    if not reviews:
        print("No reviews found for this project.")
        return
    
    print(f"Reviews for Project ({len(reviews)} total)")
    print("=" * 60)
    
    for review in reviews:
        reviewer_name = review['reviewer']['name']
        review_date = datetime.fromisoformat(review['createdAt'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
        
        print(f"\nReviewer: {reviewer_name}")
        print(f"Date: {review_date}")
        
        if review['reviewType']:
            print(f"Type: {review['reviewType']}")
        
        if review['justification']:
            print(f"Justification: {review['justification']}")
        
        print(f"Comment:")
        comment_lines = review['comment'].split('\n')
        for line in comment_lines:
            print(f"{line}")

def print_project_stats():
    r = requests.get("https://shipwrecked.hackclub.com/api/projects", headers=user_headers)
    projects = r.json()
    
    if not projects:
        print("You have no projects yet!")
        return
    
    total_projects = len(projects)
    shipped_projects = sum(1 for p in projects if p['shipped'])
    submitted_projects = sum(1 for p in projects if p['submitted'])
    viral_projects = sum(1 for p in projects if p['viral'])
    in_review_projects = sum(1 for p in projects if p['in_review'])
    total_hours = sum(p.get('rawHours', 0) for p in projects)
    
    print("Project Statistics")
    print("=" * 30)
    print(f"Total Projects: {total_projects}")
    print(f"Shipped: {shipped_projects}")
    print(f"Submitted: {submitted_projects}")
    print(f"Viral: {viral_projects}")
    print(f"In Review: {in_review_projects}")
    print(f"Total Hours: {total_hours:.1f}h")
    
    if total_projects > 0:
        print(f"Average Hours/Project: {total_hours/total_projects:.1f}h")
        print(f"Ship Rate: {(shipped_projects/total_projects)*100:.1f}%")

r_user_data()
print("\nType 'exit' to exit the program & 'help' to see the list of commands.")

while True:
    cmdl = input(generate_cmd_line()).lower()

    if cmdl == "exit":
        cmdl_exit()
    elif cmdl == "clear":
        cmdl_clear()
    elif inShop == True:
        if cmdl == "back":
            inShop = False
        elif cmdl.startswith("help"):
            print_shop_submenu_help_screen()
        elif cmdl == "items":
            print_shop_items()
        elif cmdl == "orders":
            print_shop_orders()
        elif cmdl == "inventory":
            print_shop_inventory()
        else:
            cmdl_cmd_not_found()
    elif inUser == True:
        if cmdl.startswith("help"):
            print_user_submenu_help_screen()
        elif cmdl == "back":
            inUser = False
        elif cmdl == "exit":
            cmdl_exit()
        else:
            user_submenu_commands(cmdl)
    elif inProjects == True:
        if cmdl.startswith("help"):
            print_projects_submenu_help_screen()
        elif cmdl == "back":
            inProjects = False
        elif cmdl == "list":
            print_projects_list()
        elif cmdl == "stats":
            print_project_stats()
        elif cmdl.startswith("details"):
            cmdl_parts = cmdl.split(" ")
            if len(cmdl_parts) == 2:
                print_project_details(cmdl_parts[1])
            else:
                print("Usage: details <project_id>")
        elif cmdl.startswith("reviews"):
            cmdl_parts = cmdl.split(" ")
            if len(cmdl_parts) == 2:
                print_project_reviews(cmdl_parts[1])
            else:
                print("Usage: reviews <project_id>")
        else:
            cmdl_cmd_not_found()
    elif "help" in cmdl:
        cmdl = cmdl.split(" ")
        if len(cmdl) == 2:
            if "shop" in cmdl[1]:
                print_shop_submenu_help_screen()
            elif "user" in cmdl[1]:
                print_user_submenu_help_screen()
            elif "projects" in cmdl[1]:
                print_projects_submenu_help_screen()
        elif len(cmdl) == 1:
            print("--- General commands ---")
            print("help - Show this help message")
            print("whoami - Show your user data")
            print("session - Show your session data")
            print("progress - Show your progress to the island!")
            print("leaderboard <length> - Show the leaderboard sorted by hours")
            print("fetch - Fetch your ShipwreckedCli information")
            print("logout - Delete all locally stored data")
            print("\n--- Submenus (use help <submenu> to view commands help page) ---")
            print("shop - enter the shop")
            print("user - enter the shipwrecked settings screen")
            print("projects - enter the projects submenu")
        else:
            print("Uh oh, seems like that help command was invalid.")
            print(len(cmdl))
        print("\n --- Always available commands ---")
        print("clear - Clear the screen")
        print("exit - Exit the program")
    elif cmdl == "whoami":
        whoami()
    elif cmdl == "session":
        session()
    elif cmdl == "progress":
        progress()
    elif cmdl == "shop":
        inShop = True
    elif cmdl == "user":
        inUser = True
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
            leaderboard(tmp)
        except:
            cmdl_cmd_not_found()
    elif cmdl == "fetch":
        fetch()
    elif cmdl == "projects":
        inProjects = True
    elif cmdl == "logout":
        if (input("Are you sure you want to logout? (this cant be undone) (y/n): ")).lower() == "y":
            os.remove(configfilepath)
            cmdl_exit()
    else:
        cmdl_cmd_not_found()