import requests

class ShopClassOriginal():
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr

    def print_shop_submenu_help_screen(self):
        print("--- Shop Submenu Commands ---")
        print("items - view shop items")
        print("purchase <item> - buy shop item (under construction - not working rn)")
        print("orders - view shop orders")
        print("inventory - view your fulfilled orders")
        print("back - exit back to main programm")
        print("cd .. - Return to main menu")

    def print_shop_items(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/bay/shop/items", headers=self.user_headers)
        r2 = requests.get("https://shipwrecked.hackclub.com/api/users/me/shells", headers=self.user_headers)
        data = r.json()
        shell_data = r2.json()

        print(f"Shell Shop ({shell_data["shells"]} shells available | {len(data["items"])} in shop)")
        for item in data["items"]:
            print(f"\n- {item["name"]} (id: {item["id"]}) -")
            print(item["description"])
            print(f"Price {item["price"]}")

    def print_shop_orders(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shop-orders", headers=self.user_headers)
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

    def print_shop_inventory(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/users/me/shop-orders", headers=self.user_headers)
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