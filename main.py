import os
import json
import subprocess
import openai

SECRETS_FILE = "secrets.json"

def load_api_key():
    with open(SECRETS_FILE) as f:
        secrets = json.load(f)
    return secrets["openai_api_key"]

openai.api_key = load_api_key()

def get_modified_files():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        stdout=subprocess.PIPE,
        text=True
    )
    modified = []
    for line in result.stdout.strip().splitlines():
        if line.startswith(" M") or line.startswith("A ") or line.startswith("??"):
            modified.append(line.strip().split()[-1])
    return modified

def ask_gpt_commit_message(filename):
    prompt = f"""Write a concise Git commit message for the file: {filename}. 
The message should reflect typical changes in an EAGLE PCB project 
(schematic, board layout, or Gerbers)."""
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful Git assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=60
    )
    return response.choices[0].message.content.strip()

def commit_and_push(files):
    for file in files:
        print(f"🔍 Generating commit message for {file}...")
        msg = ask_gpt_commit_message(file)
        print(f"💬 Commit message: {msg}")
        subprocess.run(["git", "add", file])
        subprocess.run(["git", "commit", "-m", msg])
    print("📤 Pushing to remote...")
    subprocess.run(["git", "push"])

def main():
    print("📁 Scanning for modified files...")
    modified_files = get_modified_files()
    if not modified_files:
        print("✅ No changes to commit.")
        return
    print(f"📝 Found {len(modified_files)} files to commit.")
    commit_and_push(modified_files)

if __name__ == "__main__":
    main()
