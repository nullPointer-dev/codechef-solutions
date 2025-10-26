import os
from datetime import datetime

# --- Config ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLVED_DIR = os.path.join(REPO_ROOT, "solved problems")

# Utility: print timestamped logs
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Ensure base folder exists
def ensure_dirs():
    if not os.path.exists(SOLVED_DIR):
        os.makedirs(SOLVED_DIR)
        log(f"Created base directory: {SOLVED_DIR}")

# Core function: create new problem folder + files
def create_problem_folder(rating, link, lang_ext):
    # e.g., rating = "823"
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
            f.write("// Solution goes here\n" if lang_ext in ["c", "cpp"] else "# Solution goes here\n")
        log(f"Created: {solution_file}")
    else:
        log(f"Solution file already exists: {solution_file}")

def main():
    ensure_dirs()

    # Example manual test (we'll automate scraping later)
    rating = input("Enter problem rating (e.g. 823): ").strip()
    link = input("Enter problem link (e.g. https://www.codechef.com/problems/START01): ").strip()
    lang = input("Language used [c/cpp/py]: ").strip().lower()

    create_problem_folder(rating, link, lang)
    log("All files created successfully!")

if __name__ == "__main__":
    main()
