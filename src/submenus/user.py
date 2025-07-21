import requests

class UserClassOriginal():
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr

    def print_user_submenu_help_screen(self):
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
        print("cd .. - Return to main menu")

    def user_submenu_commands(self, field):
        r = requests.get("https://shipwrecked.hackclub.com/api/identity/me", headers=self.user_headers)
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
            print("Uh oh, seems like there was an error I couldn't quite catch!")