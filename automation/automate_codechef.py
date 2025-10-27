import os
import requests
from bs4 import BeautifulSoup
from git import Repo
from datetime import datetime

# --- CONFIG ---
REPO_PATH = r"C:\Users\Sashank\Documents\codechef-solutions"
SOLVED_DIR = os.path.join(REPO_PATH, "solved problems")
USERNAME = "shary_snow_21"
PROFILE_API = f"https://www.codechef.com/api/user/{USERNAME}"

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def ensure_dirs():
    if not os.path.exists(SOLVED_DIR):
        os.makedirs(SOLVED_DIR)
        log(f"Created base directory: {SOLVED_DIR}")

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
            f.write("// Solution goes here\n" if lang_ext != "py" else "# Solution goes here\n")
        log(f"Created: {solution_file}")
    else:
        log(f"Solution file already exists: {solution_file}")

def scrape_solved_problems():
    response = requests.get(PROFILE_API, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        print("❌ Failed to fetch data:", response.status_code)
        return []

    data = response.json()
    fully_solved = data.get("fully_solved", {})
    solved = []

    for category in fully_solved.values():
        for p in category:
            code = p.get("problem_code")
            rating = str(p.get("problem_rating", "unrated"))
            link = f"https://www.codechef.com/problems/{code}"
            solved.append({"rating": rating, "link": link})

    print(f"✅ Found {len(solved)} solved problems.")
    return solved

def git_commit_and_push(commit_msg="Add new solved problems"):
    repo = Repo(REPO_PATH)
    repo.git.add(A=True)

    if repo.is_dirty():
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
    for p in problems:
        create_problem_folder(p["rating"], p["link"], "py")

    git_commit_and_push()

if __name__ == "__main__":
    main()
