import requests
from datetime import datetime, timezone

class FetchClassOriginal():
    def __init__(self):
        self.user_headers = ""
        self.version = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr

    def set_ver(self, ver):
        self.version = ver

    def fetch(self, user):
        user_data = user
            
        progress_r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shells", headers=self.user_headers)
        progress_data = progress_r.json()
            
        session_r = requests.get("https://shipwrecked.hackclub.com/api/auth/session", headers=self.user_headers)
        session_data = session_r.json()
            
        target_time = datetime.fromisoformat(session_data['expires'])
        current_time = datetime.now(timezone.utc)
        time_diff = target_time - current_time
        days = time_diff.days
        hours = time_diff.seconds // 3600
            
        orders_r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shop-orders", headers=self.user_headers)
        orders_data = orders_r.json()
        total_orders = len(orders_data["orders"])
        fulfilled_orders = sum(1 for order in orders_data["orders"] if order["status"] == "fulfilled")
            
        ascii_art = """
        SHIPWRECKED CLI v""" + self.version + """
    ═══════════════════════════════
        Welcome aboard, sailor!
        """
            
        print(ascii_art)
        print(f"    User: {user_data['name']}")
        print(f"    Email: {user_data['email']}")
        print(f"    ID: {user_data['id']}")
        print(f"    Shells: {progress_data['shells']} (earned: {progress_data['earnedShells']}, spent: {progress_data['totalSpent']})")
        print(f"    Progress: {progress_data['progress']['total']['percentage']:.1f}%")
        print(f"    Orders: {total_orders} total ({fulfilled_orders} fulfilled)")
        print(f"    Session: {days}d {hours}h remaining")
        print(f"    Admin: {'Yes' if user_data.get('isAdmin', False) else 'No'}")
        print(f"    Shop Admin: {'Yes' if user_data.get('isShopAdmin', False) else 'No'}")
        print(f"    Slack: {'Connected' if user_data.get('slack') else 'Not connected'}")
        print(f"    Verified: {'Yes' if user_data.get('emailVerified', False) else 'No'}")
        print()
        print("    ═══════════════════════════════")
        print("    Developed with ♥ by LennyMaxMine")
        print(" Frankfurt, Germany | HC Shipwrecked 2025")
        print("    ═══════════════════════════════")
        print()