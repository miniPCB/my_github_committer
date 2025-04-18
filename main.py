import os
import json
import subprocess
import openai

SECRETS_FILE = "secrets.json"
CONFIG_FILE = "config.json"

def load_api_key():
    with open(SECRETS_FILE) as f:
        secrets = json.load(f)
    return secrets["openai_api_key"]

openai.api_key = load_api_key()

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"favorites": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def list_subfolders(path):
    try:
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    except PermissionError:
        return []

def select_git_repo():
    current_path = "C:\\"
    while True:
        subfolders = list_subfolders(current_path)
        print(f"\n📂 Current folder: {current_path}")
        print("0. [Select this folder]")
        for i, folder in enumerate(subfolders, 1):
            print(f"{i}. {folder}")
        print("B. [Back]")

        choice = input("Select folder: ").strip().upper()

        if choice == "0":
            if os.path.isdir(os.path.join(current_path, ".git")):
                return current_path
            else:
                print("❌ Not a Git repository. Try another folder.")
        elif choice == "B":
            parent = os.path.dirname(current_path.rstrip("\\"))
            if parent and parent != current_path:
                current_path = parent
        elif choice.isdigit() and 1 <= int(choice) <= len(subfolders):
            current_path = os.path.join(current_path, subfolders[int(choice) - 1])
        else:
            print("❓ Invalid choice.")

def select_git_repo_with_favorites():
    config = load_config()
    favorites = config.get("favorites", [])

    while True:
        print("\n⭐ Favorite Git Repos:")
        for i, path in enumerate(favorites, 1):
            print(f"{i}. {path}")
        print("B. [Browse for new folder]")

        choice = input("Select repo or browse: ").strip().upper()

        if choice == "B":
            path = select_git_repo()
            if path not in favorites:
                add = input("💾 Add to favorites? (y/n): ").strip().lower()
                if add == "y":
                    favorites.append(path)
                    config["favorites"] = favorites
                    save_config(config)
            return path
        elif choice.isdigit() and 1 <= int(choice) <= len(favorites):
            return favorites[int(choice) - 1]
        else:
            print("❓ Invalid choice.")

def get_modified_files(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "status", "--porcelain"],
        stdout=subprocess.PIPE,
        text=True
    )
    modified = []
    for line in result.stdout.strip().splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        filename = line[3:] if line[2] == ' ' else line[2:].strip()
        modified.append(filename)
    return modified

def has_unmerged_files(repo_path):
    result = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"],
                            stdout=subprocess.PIPE, text=True)
    for line in result.stdout.strip().splitlines():
        if line.startswith("U"):
            return True
    return False

def is_branch_behind(repo_path):
    subprocess.run(["git", "-C", repo_path, "fetch"])
    result = subprocess.run(["git", "-C", repo_path, "status"],
                            stdout=subprocess.PIPE, text=True)
    return "behind" in result.stdout

def offer_pull(repo_path):
    if is_branch_behind(repo_path):
        print("🔄 Your branch is behind the remote.")
        choice = input("Do you want to pull the latest changes first? (y/n): ").strip().lower()
        if choice == 'y':
            subprocess.run(["git", "-C", repo_path, "pull"])

def ask_gpt_commit_message(filename):
    prompt = f"""Write a concise Git commit message for the file: {filename}. 
The message should reflect typical changes in an EAGLE PCB project 
(schematic, board layout, or Gerbers)."""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful Git assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=60
    )
    return response.choices[0].message.content.strip()

def commit_and_push(files, repo_path):
    for file in files:
        print(f"🔍 Generating commit message for {file}...")
        msg = ask_gpt_commit_message(file)
        print(f"💬 Commit message: {msg}")
        result = subprocess.run(["git", "-C", repo_path, "add", file])
        subprocess.run(["git", "-C", repo_path, "commit", "-m", msg])

    offer_pull(repo_path)

    print("📤 Pushing to remote...")
    subprocess.run(["git", "-C", repo_path, "push"])

def main():
    repo_path = select_git_repo_with_favorites()
    print(f"✅ Selected Git repo: {repo_path}")

    if has_unmerged_files(repo_path):
        print("❌ Merge conflicts detected. Please resolve them before committing.")
        return

    modified_files = get_modified_files(repo_path)
    if not modified_files:
        print("✅ No changes to commit.")
        return

    print(f"📝 Found {len(modified_files)} files to commit.")
    commit_and_push(modified_files, repo_path)

if __name__ == "__main__":
    main()
