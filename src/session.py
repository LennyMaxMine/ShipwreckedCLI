import requests
from datetime import datetime, timezone

class SessionClassOriginal():
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr

    def session(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/auth/session", headers=self.user_headers)
        
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