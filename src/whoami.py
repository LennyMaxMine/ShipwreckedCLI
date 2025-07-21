class WhoamiClassOriginal():
    def whoami(self, user_data):
        tmp_user_data = user_data
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