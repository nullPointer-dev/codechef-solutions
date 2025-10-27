import os
import requests
from bs4 import BeautifulSoup
from git import Repo

import os
from datetime import datetime

# --- CONFIG ---
REPO_PATH = r"C:\Users\Sashank\Documents\codechef-solutions"  # root of your repo
SOLVED_DIR = os.path.join(REPO_PATH, "solved problems")

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Ensure base folder exists
def ensure_dirs():
    if not os.path.exists(SOLVED_DIR):
        os.makedirs(SOLVED_DIR)
        log(f"Created base directory: {SOLVED_DIR}")

# Core function: create folder + prob.md + solution file
def create_problem_folder(rating, link, lang_ext):
    folder_name = f"{rating}-codechef"
    folder_path = os.path.join(SOLVED_DIR, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        log(f"Created folder: {folder_path}")
    else:
        log(f"Folder already exists: {folder_path}")

    # Create prob.md
    prob_md_path = os.path.join(folder_path, "prob.md")
    with open(prob_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Problem Link\n\n{link}\n")
    log(f"Created: {prob_md_path}")

    # Create empty solution file
    solution_file = os.path.join(folder_path, f"{folder_name}.{lang_ext}")
    if not os.path.exists(solution_file):
        with open(solution_file, "w", encoding="utf-8") as f:
            f.write("# Solution goes here\n" if lang_ext=="py" else "// Solution goes here\n")
        log(f"Created: {solution_file}")
    else:
        log(f"Solution file already exists: {solution_file}")

# CONFIG
USERNAME = "nullPointer-dev"
SESSION_COOKIE = "<AKEyXzUMmcORsdCtXOg6c6aWsR3_EDwB2F_dhx7Iz2YrH6cE2vWl7vQuksPQ4L6CMUgzM6v3Q2rN>"
REPO_PATH = r"C:\Users\Sashank\Documents\codechef-solutions"  # root of your repo

# Create a requests session
session = requests.Session()

# Add headers to mimic a browser
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.7204.243 Safari/537.36"
})

from bs4 import BeautifulSoup

def scrape_solved_problems():
    url = f"https://www.codechef.com/users/{USERNAME}"
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch profile: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    problems = []
    # Find the section that contains solved problems
    # NOTE: Adjust selectors according to actual HTML structure
    table = soup.find("div", {"class": "dataTable"})
    if not table:
        print("Could not find solved problems section.")
        return []

    for link_tag in table.find_all("a"):
        problem_link = "https://www.codechef.com" + link_tag.get("href")
        problem_name = link_tag.text.strip()
        # Extract rating from problem name if included (like "823 START01")
        rating = problem_name.split()[0]  # assumes first part is numeric
        problems.append({"rating": rating, "link": problem_link})

    print(f"Found {len(problems)} solved problems.")
    return problems

def git_commit_and_push(commit_msg="Add new solved problems"):
    repo = Repo(REPO_PATH)       # REPO_PATH should point to your repo root
    repo.git.add(A=True)         # Stage all changes

    if repo.is_dirty():          # Check if there’s something new to commit
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ Changes committed and pushed to GitHub!")
    else:
        print("No changes to commit. Repo is up to date.")


def main():
    print("Starting automation...")
    ensure_dirs()
    
    problems = scrape_solved_problems()
    print(f"✅ Found {len(problems)} problems.") 
    for p in problems:
        print(f"→ {p['rating']}: {p['link']}")
        create_problem_folder(p["rating"], p["link"], "py")  # or your language choice

    # Auto commit & push after creating folders
    git_commit_and_push()



if __name__ == "__main__":
    main()
