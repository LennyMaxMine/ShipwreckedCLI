import requests
from typing import List, Dict, Any
from datetime import datetime

class LeaderboardOriginal:
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr
        
    def leaderboard(self, stored_user_name, top: int):
        r = requests.get("https://shipwrecked.hackclub.com/api/users")
        self.generate_leaderboard(r.json(), top_n=top, highlight_name=stored_user_name)

    def generate_leaderboard(self, data, top_n: int = 10, highlight_name: str = None):
        leaderboard = []
        
        for user in data:
            name = user.get('name', 'Anonymous')
            total_hours = 0
            
            for project in user.get('projects', []):
                for link in project.get('hackatimeLinks', []):
                    hours = link.get('hoursOverride') or link.get('rawHours', 0)
                    total_hours += hours
            
            in_review_count = sum(1 for project in user.get('projects', []) if project.get('in_review', False))
            
            created_at = user.get('createdAt', '')
            if created_at:
                try:
                    date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    joined_date = date_obj.strftime('%b %d, %Y')
                except:
                    joined_date = 'Unknown'
            else:
                joined_date = 'Unknown'
            
            if total_hours > 0:
                leaderboard.append({
                    'name': name,
                    'total_hours': total_hours,
                    'projects_count': len(user.get('projects', [])),
                    'in_review_count': in_review_count,
                    'joined_date': joined_date
                })
        
        leaderboard.sort(key=lambda x: x['total_hours'], reverse=True)
        
        highlighted_user = None
        highlighted_rank = None
        if highlight_name:
            highlight_name_lower = highlight_name.lower()
            for i, user in enumerate(leaderboard):
                user_name = user['name']
                if user_name and user_name.lower() == highlight_name_lower:
                    highlighted_user = user
                    highlighted_rank = i + 1
                    break
        
        top_users = leaderboard[:top_n]
        
        if highlighted_user and highlighted_user not in top_users:
            top_users.append(highlighted_user)
        
        self.print_leaderboard_table(top_users, highlight_name, highlighted_rank, leaderboard)

    def print_leaderboard_table(self, leaderboard, highlight_name: str = None, highlighted_rank: int = None, full_leaderboard: list = None):
        if not leaderboard:
            print("No users with logged hours found.")
            return
        
        print("\nShipwrecked Leaderboard")
        print("=" * 80)
        
        print(f"{'Rank':<4} {'Name':<20} {'Hours':<8} {'Seashells':<10} {'In Review':<10} {'Joined':<12}")
        print("-" * 80)
        
        highlight_name_lower = highlight_name.lower() if highlight_name else None
        
        for i, user in enumerate(leaderboard, 1):
            user_name = user['name']
            is_highlighted = highlight_name_lower and user_name and user_name.lower() == highlight_name_lower
            
            if is_highlighted and highlighted_rank:
                rank = f"#{highlighted_rank}"
            else:
                rank = f"#{i}"
                
            user_name = user['name'] or 'Anonymous'
            name = user_name[:19] if len(user_name) > 19 else user_name
            hours = f"{user['total_hours']:.2f}"
            clamshells = str(user['projects_count'])
            in_review = str(user['in_review_count'])
            joined = user['joined_date'][:11] if len(user['joined_date']) > 11 else user['joined_date']
            
            if is_highlighted:
                print(f"\033[1m{rank:<4} {name:<20} {hours:<8} {clamshells:<10} {in_review:<10} {joined:<12}\033[0m")
            else:
                print(f"{rank:<4} {name:<20} {hours:<8} {clamshells:<10} {in_review:<10} {joined:<12}")
        
        print("=" * 80)