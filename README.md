# --- STEP 1: Final File Preparation ---

# 1. Ensure requirements.txt is created with all installed packages (Flask, google-genai, etc.)
# This file is critical for dependency management.
(venv) pip freeze > requirements.txt

# 2. Ensure your .gitignore file contains these lines to protect your key and keep the repo clean.
# Use an editor like VS Code or Notepad to confirm your existing .gitignore contains:
# venv/
# .env
# __pycache__/

# --- STEP 2: Initialize Git and Link to GitHub ---

# 3. Initialize the Git repository in your project folder (if you haven't already).
# If git init returns "Reinitialized existing Git repository...", you can skip this.
(venv) git init

# 4. Link your local project to the empty remote repository you created on GitHub.
# **NOTE: Replace [YOUR-GITHUB-USERNAME] and [YOUR-REPO-NAME] with your actual information.**
(venv) git remote add origin https://github.com/[YOUR-GITHUB-USERNAME]/[YOUR-REPO-NAME].git

# --- STEP 3: Commit and Push to GitHub (The Final Deliverable) ---

# 5. Stage all files (app.py, README.md, requirements.txt, .gitignore). 
# Files listed in .gitignore (.env, venv/) will be automatically skipped.
(venv) git add .

# 6. Commit the staged files with a descriptive message.
(venv) git commit -m "Final submission commit: Smart Task Planner API implemented and documentation added."

# 7. Push all files to the 'main' branch of your GitHub repository.
(venv) git push -u origin main

# --- STEP 4: Final Deliverable URL ---

# 8. Copy the URL of your GitHub repository. This is one of the required deliverables.
https://github.com/tsnteja12/Smart_Task_Planner.git

# --- STEP 5: Demo Video Reminder ---

# [cite_start]9. Record your Demo video as required[cite: 16].
# The video must demonstrate the system processing a NEW goal and highlighting the structured JSON output (task breakdown, dependencies, and estimated timelines).