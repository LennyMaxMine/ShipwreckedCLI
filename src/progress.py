import requests

class ProgressClassOriginal():
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr

    def progress(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shells", headers=self.user_headers)
        data = r.json()

        print(f"Island Progress: {data["progress"]["total"]["percentage"]}% (earned: {data["progress"]["total"]["percentage"] - data["progress"]["purchased"]["percentage"]} | purchased {data["progress"]["purchased"]["percentage"]})")
        print(f"Shells: {data["shells"]} (earned: {data["earnedShells"]} | spent: {data["totalSpent"]})")
