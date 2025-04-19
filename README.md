### ✅ Summary of What the Script Does

This Python script is an interactive assistant that helps users select a Git repository (with support for favorites), generate AI-powered commit messages using OpenAI's GPT model based on diffs, and automatically commit and push modified files. It also performs smart checks such as detecting unmerged files or whether the local branch is behind the remote.

---

### 🧠 Code Explanation – Section by Section

#### 1. ⚙️ API Key and Configuration Management

```python
def load_api_key():
    with open(SECRETS_FILE) as f:
        secrets = json.load(f)
    return secrets["openai_api_key"]
```

- Loads the OpenAI API key from `secrets.json`.

```python
def load_config():
    ...
def save_config(config):
    ...
```

- Handles reading and saving user configuration such as favorite repos from/to `config.json`.

---

#### 2. 📁 Folder/File Selector

```python
def list_subfolders(path):
```

- Lists subdirectories at a given path, ignoring inaccessible ones.

```python
def select_git_repo():
```

- Presents a terminal UI to navigate Windows directories interactively and lets the user select a Git repository folder.

```python
def select_git_repo_with_favorites():
```

- Displays a menu of saved favorite repos, allows browsing for new ones, tagging them as "eagle" or "generic", and optionally saving to favorites.

---

#### 3. 🔍 Commit Message Generation with OpenAI

```python
def ask_gpt_commit_message(filename, repo_path, repo_type):
```

- Checks if a file is suitable for generating a commit message (ignores binaries).
- Retrieves Git diff for the file.
- Prompts OpenAI's GPT model with file diffs and context based on the repo type (EAGLE or generic).
- Returns a suggested commit message.

---

#### 4. 📄 Git Status Utilities

```python
def get_modified_files(repo_path):
```

- Lists modified or untracked files in a repository.

```python
def has_unmerged_files(repo_path):
```

- Checks for unresolved merge conflicts.

```python
def is_branch_behind(repo_path):
```

- Uses `git fetch` and checks if the local branch is behind the remote.

```python
def offer_pull(repo_path):
```

- Offers the user an option to `git pull` if the branch is behind.

---

#### 5. ✔️ Commit and Push Changes

```python
def commit_and_push(files, repo_path, repo_type):
```

- For each modified file:
  - Generates AI-assisted message
  - Stages the file
  - Commits it
- Optionally pulls the latest changes
- Pushes everything to the remote repository

---

#### 6. 🚀 Main Function

```python
def main():
```

- Launches the repo selector
- Checks for merge conflicts
- Gets modified files
- Calls the commit-push logic

---

### 📘 README-Style Documentation

---

## 🧠 GitGPT: AI-Powered Git Commit Assistant

An interactive Python CLI assistant that helps you write concise and context-aware Git commit messages using OpenAI's GPT models.

### 🚀 Overview

GitGPT is a command-line tool that:
- Helps you select your Git repositories easily
- Saves repository favorites for fast access
- Uses GPT-based AI to create smart commit messages based on diffs
- Supports EAGLE PCB projects and generic code/document repos
- Auto-commits and pushes changes to your remote

---

### ✅ Features

- 🧠 Uses OpenAI GPT to generate commit messages tailored to diffs
- 🗂 Interactive Git repo browser with support for favorites
- 🛠 Detects modified/untracked files, merge conflicts, and sync status
- 🔄 Optionally performs `git pull` if behind the remote
- 📦 Lightweight and non-intrusive CLI utility

---

### ▶️ How to Run

1. **Install Dependencies**

```bash
pip install openai
```

2. **Create Required Files**

- `secrets.json` should contain your OpenAI API key:

```json
{
  "openai_api_key": "sk-..."
}
```

- (Optionally) Add a `config.json` to store favorites, or let the tool create one automatically.

3. **Run the Script**

```bash
python git_gpt_assistant.py
```

---

### 💡 Example Usage

1. On running, you'll be prompted to select from favorite Git repositories or browse for a new one.
2. For each modified file, the script:
   - Shows diff output (if available)
   - Sends it to GPT-4 to get a commit message suggestion
   - Stages and commits the file using that message
3. You are asked whether to perform a `git pull` if the local branch is behind the remote.
4. Commits are pushed to the project’s remote.

---

### 📌 Notes

- Supports two repo types:
  - `eagle` — for PCB design projects
  - `generic` — for regular code/content
- Binary or non-text files (e.g., `.png`, `.zip`) are auto-skipped.
- Requires Python 3.7+

---

Enjoy committing smarter with GitGPT! 🧠✨