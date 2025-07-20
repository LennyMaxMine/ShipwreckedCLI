import requests

def login(email):
    csrf_req = requests.get("https://shipwrecked.hackclub.com/api/auth/csrf")
    csrf_req_json = csrf_req.json()
    print(csrf_req.status_code)

    payload = {
        "email" : email,
        "callbackURL" : "/bay/login/success",
        "csrfToken" : csrf_req_json["csrfToken"],
        "json" : True
    }

    signin_req = requests.get(f"https://shipwrecked.hackclub.com/api/auth/signin/email", params=payload)

    print(signin_req.status_code)
    print(signin_req.json())

    print("Check email")
    input("Copy the signin link and enter it here: ")

# USELESS :(