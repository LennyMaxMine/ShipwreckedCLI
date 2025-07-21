import requests
from datetime import datetime


class ProjectsClassOriginal():
    def __init__(self):
        self.user_headers = ""

    def set_user_hdr(self, usr_hdr):
        self.user_headers = usr_hdr

    def print_projects_submenu_help_screen(self):
        print("--- Projects Submenu Commands ---")
        print("list - View all your projects")
        print("details <project_id> - View detailed project information")
        print("reviews <project_id> - View project reviews")
        print("stats - Show project statistics")
        print("back - exit back to main program")
        print("cd .. - Return to main menu")


    def print_projects_list(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/projects", headers=self.user_headers)
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

    def print_project_details(self, project_id):
        r = requests.get("https://shipwrecked.hackclub.com/api/projects", headers=self.user_headers)
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

    def print_project_reviews(self, project_id):
        r = requests.get(f"https://shipwrecked.hackclub.com/api/reviews?projectId={project_id}", headers=self.user_headers)
        
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

    def print_project_stats(self):
        r = requests.get("https://shipwrecked.hackclub.com/api/projects", headers=self.user_headers)
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
