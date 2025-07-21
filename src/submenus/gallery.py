import requests
from datetime import datetime

class GalleryClassOriginal():
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr
        
    def print_gallery_submenu_help_screen(self):
        print("--- Gallery Submenu Commands ---")
        print("list <amount> - View <amount> gallery projects")
        print("details <project_id> - View detailed project information")
        print("upvote <project_id> - Upvote a project")
        print("popular - View projects sorted by upvotes")
        print("recent - View projects by most recent chat activity")
        print("search <term> - Search projects by name or description")
        print("stats - Show gallery statistics")
        print("back - exit back to main program")
        print("cd .. - Return to main menu")

    def print_gallery_list(self, limit: int = 10):
        r = requests.get("https://shipwrecked.hackclub.com/api/gallery", headers=self.user_headers)
        projects = r.json()
        
        if not projects:
            print("No projects in gallery!")
            return
        
        print(f"Gallery Projects (showing up to {min(limit, len(projects))} of {len(projects)} total)")
        print("=" * 60)
        
        for project in projects[:limit]:
            user_name = project['user']['name'] if project['user']['name'] else "Anonymous"
            hours = project.get('rawHours', 0)
            upvotes = project.get('upvoteCount', 0)
            chats = project.get('chatCount', 0)
            
            status_icons = []
            if project["shipped"]: status_icons.append("Shipped")
            if project["viral"]: status_icons.append("Viral")
            if project["chat_enabled"]: status_icons.append("Chat")
            
            status_text = " | ".join(status_icons) if status_icons else "Draft"
            
            print(f"\n--- {project['name']} by {user_name} (id: {project['projectID']}) ---")
            print(f"{project['description']}")
            print(f"Hours: {hours:.1f}h | Upvotes: {upvotes} | Chats: {chats}")
            
            if project.get('codeUrl'):
                print(f"Code: {project['codeUrl']}")
            if project.get('playableUrl'):
                print(f"Demo: {project['playableUrl']}")

    def print_gallery_project_details(self,project_id):
        r = requests.get("https://shipwrecked.hackclub.com/api/gallery", headers=self.user_headers)    
        projects = r.json()
        project = next((p for p in projects if p['projectID'] == project_id), None)
        
        if not project:
            print(f"Project with ID '{project_id}' not found in gallery!")
            return
        
        user_name = project['user']['name'] if project['user']['name'] else "Anonymous"
        user_slack = project['user']['slack'] if project['user']['slack'] else "Not connected"
        user_hackatime = project['user']['hackatimeId'] if project['user']['hackatimeId'] else "N/A"
        
        print(f"Gallery Project Details: {project['name']}")
        print("=" * 60)
        print(f"ID: {project['projectID']}")
        print(f"Description: {project['description']}")
        print(f"Creator: {user_name} (Slack: {user_slack}, Hackatime: {user_hackatime})")
        print(f"Total Hours: {project.get('rawHours', 0):.2f}h")
        print(f"Upvotes: {project.get('upvoteCount', 0)} {'(You upvoted!)' if project.get('userUpvoted', False) else ''}")
        print(f"Chat Messages: {project.get('chatCount', 0)}")
        
        if project.get('lastChatActivity'):
            last_chat = datetime.fromisoformat(project['lastChatActivity'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            print(f"Last Chat Activity: {last_chat}")

        print(f"\nStatus:")
        print(f"Shipped: {'Yes' if project['shipped'] else 'No'}")
        print(f"Viral: {'Yes' if project['viral'] else 'No'}")
        print(f"Chat Enabled: {'Yes' if project['chat_enabled'] else 'No'}")

        print(f"\nLinks:")
        if project.get('codeUrl'):
            print(f"Code: {project['codeUrl']}")
        else:
            print("Code: Not provided")
        if project.get('playableUrl'):
            print(f"Demo: {project['playableUrl']}")
        else:
            print("Demo: Not provided")
        if project.get('screenshot'):
            print(f"Screenshot: {project['screenshot']}")

        if project.get('hackatimeLinks'):
            print(f"\nHackatime Breakdown:")
            for link in project['hackatimeLinks']:
                hours = link.get('hoursOverride') or link.get('rawHours', 0)
                print(f"• {link['hackatimeName']}: {hours:.2f}h")

    def print_gallery_popular(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/gallery", headers=self.user_headers)
        projects = r.json()
        
        # Sort by upvotes (descending)
        sorted_projects = sorted(projects, key=lambda x: x.get('upvoteCount', 0), reverse=True)
        
        print("Most Popular Projects (by upvotes)")
        print("=" * 40)
        
        for i, project in enumerate(sorted_projects[:10], 1):
            user_name = project['user']['name'] if project['user']['name'] else "Anonymous"
            upvotes = project.get('upvoteCount', 0)
            hours = project.get('rawHours', 0)
            
            print(f"{i}. {project['name']} by {user_name} (id: {project["projectID"]})")
            print(f"{upvotes} upvotes | {hours:.1f}h")
            print(f"{project['description']}")
            print()

    def print_gallery_recent(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/gallery", headers=self.user_headers)
        projects = r.json()
        
        projects_with_activity = [p for p in projects if p.get('lastChatActivity')]
        sorted_projects = sorted(projects_with_activity, 
                            key=lambda x: x['lastChatActivity'], reverse=True)
        
        print("Recently Active Projects (by chat activity)")
        print("=" * 45)
        
        for project in sorted_projects[:10]:
            user_name = project['user']['name'] if project['user']['name'] else "Anonymous"
            last_chat = datetime.fromisoformat(project['lastChatActivity'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            chat_count = project.get('chatCount', 0)
            
            print(f"• {project['name']} by {user_name} (id: {project["projectID"]})")
            print(f"Last activity: {last_chat} ({chat_count} messages)")
            print()

    def search_gallery(self, search_term):
        r = requests.get("https://shipwrecked.hackclub.com/api/gallery", headers=self.user_headers)
        
        if r.status_code != 200:
            print("Error fetching gallery data")
            return
            
        projects = r.json()
        
        matching_projects = []
        for project in projects:
            if (search_term.lower() in project['name'].lower() or 
                search_term.lower() in project['description'].lower()):
                matching_projects.append(project)
        
        if not matching_projects:
            print(f"No projects found matching '{search_term}'")
            return
        
        print(f"Search Results for '{search_term}' ({len(matching_projects)} found)")
        print("=" * 50)
        
        for project in matching_projects:
            user_name = project['user']['name'] if project['user']['name'] else "Anonymous"
            upvotes = project.get('upvoteCount', 0)
            hours = project.get('rawHours', 0)
            
            print(f"• {project['name']} by {user_name} (id: {project["projectID"]})")
            print(f"{project['description']}")
            print(f"{upvotes} upvotes | {hours:.1f}h")
            print()

    def print_gallery_stats(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/gallery", headers=self.user_headers)
        
        if r.status_code != 200:
            print("Error fetching gallery data")
            return
            
        projects = r.json()
        
        if not projects:
            print("No projects in gallery!")
            return
        
        total_projects = len(projects)
        shipped_projects = sum(1 for p in projects if p['shipped'])
        viral_projects = sum(1 for p in projects if p['viral'])
        chat_enabled = sum(1 for p in projects if p['chat_enabled'])
        total_upvotes = sum(p.get('upvoteCount', 0) for p in projects)
        total_hours = sum(p.get('rawHours', 0) for p in projects)
        total_chats = sum(p.get('chatCount', 0) for p in projects)
        
        most_upvoted = max(projects, key=lambda x: x.get('upvoteCount', 0))
        most_hours = max(projects, key=lambda x: x.get('rawHours', 0))
        
        print("Gallery Statistics")
        print("=" * 30)
        print(f"Total Projects: {total_projects}")
        print(f"Shipped Projects: {shipped_projects}")
        print(f"Viral Projects: {viral_projects}")
        print(f"Chat Enabled: {chat_enabled}")
        print(f"Total Upvotes: {total_upvotes}")
        print(f"Total Hours: {total_hours:.1f}h")
        print(f"Total Chat Messages: {total_chats}")
        
        if total_projects > 0:
            print(f"Average Hours/Project: {total_hours/total_projects:.1f}h")
            print(f"Average Upvotes/Project: {total_upvotes/total_projects:.1f}")
            print(f"Ship Rate: {(shipped_projects/total_projects)*100:.1f}%")
        
        print(f"\nMost Popular: '{most_upvoted['name']}' with {most_upvoted.get('upvoteCount', 0)} upvotes")
        print(f"Most Hours: '{most_hours['name']}' with {most_hours.get('rawHours', 0):.1f}h")

    def upvote_project(self, project_id: str):
        project_id = project_id.strip(); project_id = project_id.replace(" ", "")
        r = requests.post(f"https://shipwrecked.hackclub.com/api/projects/{project_id}/upvote", headers=self.user_headers)
        data = r.json()

        if data["upvoted"] == True:
            print(f"Upvoted succesfully! (This Project now has {data["upvoteCount"]} upvotes)")
        else:
            print(f"Upvote removed succesfully! (This Project now has {data["upvoteCount"]} upvotes)")