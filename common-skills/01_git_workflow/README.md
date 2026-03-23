# 01 — Git Workflow

Git tracks changes to your code over time. GitHub hosts your repo online and adds collaboration tools (PRs, issues, Actions). Git is the tool; GitHub is the website — they're separate things.

---

## Mental Model

Git stores your project as a timeline of **snapshots** (commits). You control when snapshots are taken and can go back to any of them.

```
main:   A ── B ── C ── D       ← each letter = one commit (snapshot)
                  │
feature:          C ── E ── F  ← branch = your own timeline
```

A **branch** is just a movable pointer to a commit. Branching spins off your own timeline so you can work without touching `main`.

---

## Setup (one time)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@email.com"
git config --global core.editor "code --wait"   # VS Code as default editor
git config --global init.defaultBranch main      # use 'main', not 'master'
```

Verify:
```bash
git config --list
```

---

## Starting a Repo

```bash
# Track an existing folder
git init

# Download an existing repo from GitHub
git clone git@github.com:user/repo.git
git clone git@github.com:user/repo.git my-folder  # clone into a custom name
```

---

## The Three Zones

This is the most important thing to understand about Git.

```
Working Directory  →  Staging Area (Index)  →  Repository
  (your files)           (git add)               (git commit)
```

| Zone | What it is |
|---|---|
| Working Directory | Your actual files on disk — edits happen here |
| Staging Area | A draft of your next commit — you choose exactly what goes in |
| Repository | Permanent history — once committed, it's safe |

---

## The Core Loop

This is 90% of daily Git:

```bash
# 1. Check what changed
git status

# 2. Stage what belongs in the next commit
git add filename.py          # one file
git add src/                 # whole folder
git add .                    # everything changed (use carefully)
git add -p                   # interactive — pick specific lines/hunks

# 3. Commit with a clear message
git commit -m "Add login form validation"

# 4. Repeat
```

**Good commit messages:** short imperative verb, present tense — "Add", "Fix", "Remove", not "Added" or "Fixed".

---

## Viewing History

```bash
git log                           # full log
git log --oneline                 # one line per commit
git log --oneline --graph         # visual branch graph
git log --oneline -10             # last 10 commits
git log --oneline --graph --all   # all branches at once

git show abc1234                  # see what changed in one commit
git diff                          # unstaged changes vs last commit
git diff --staged                 # staged changes vs last commit
git diff main..feature-branch     # compare two branches
git blame filename.py             # who last changed each line
```

---

## Branching

```bash
git branch                        # list local branches (* = current)
git branch -a                     # list all (including remote)

git switch -c feature/add-login   # create AND switch (preferred)
git switch main                   # go back to main
git branch -d feature/add-login   # delete after merging
git branch -D feature/add-login   # force delete (unmerged)
```

**Branch naming conventions:**
- `feature/add-login` — new feature
- `fix/null-pointer-crash` — bug fix
- `refactor/clean-auth` — cleanup/refactor
- `chore/update-deps` — non-code maintenance

---

## Merging and Rebasing

Both get changes from one branch into another — different approaches.

### Merge (safe, preserves history)
```bash
git switch main
git merge feature/add-login
```
Creates a **merge commit** joining the two timelines. History shows exactly what happened and when.

### Rebase (linear history, rewrites commits)
```bash
git switch feature/add-login
git rebase main            # replay your commits on top of current main
```
Rewrites your branch's commits as if they started from the tip of `main`. Gives a clean, linear log. **Never rebase a branch others are using** — you'll rewrite history they've built on.

---

## Undoing Things

### Unstaged changes (before `git add`)
```bash
git restore filename.py    # discard edits to one file ⚠️ irreversible
git restore .              # discard ALL unstaged edits ⚠️ irreversible
```

### Unstage a file (after `git add`, before commit)
```bash
git restore --staged filename.py
```

### Undo the last commit (keep the work)
```bash
git reset --soft HEAD~1    # uncommit, keep changes staged
git reset HEAD~1           # uncommit, keep changes in working dir (unstaged)
```

### Undo the last commit (throw away changes) ⚠️
```bash
git reset --hard HEAD~1    # permanently deletes those changes
```

### Fix the last commit (before pushing only)
```bash
git commit --amend         # change message or add forgotten files
```

### Revert a commit that's already pushed
```bash
git revert abc1234         # creates a NEW commit that undoes the old one — safe
```

> **Rule:** `reset` rewrites history (only safe before pushing). `revert` adds a new "undo" commit (safe anytime).

---

## Stashing

Save work-in-progress without committing:

```bash
git stash                           # stash staged + unstaged changes
git stash push -m "wip: auth form"  # stash with a label
git stash list                      # see all stashes
git stash pop                       # restore latest stash and delete it
git stash apply stash@{1}           # restore specific stash, keep it in list
git stash drop stash@{1}            # delete a specific stash
git stash clear                     # delete all stashes ⚠️
```

**When to use:** You're mid-feature and need to switch branches quickly without committing half-done work.

---

## .gitignore

Tells Git which files to never track. Put it in the project root.

```gitignore
# Python
__pycache__/
*.pyc
.venv/

# C++
*.o
*.exe
main

# General
.DS_Store
.env
node_modules/
```

After adding to `.gitignore`, check it's working:
```bash
git status --ignored
```

If a file is already tracked and you add it to `.gitignore`, you need to stop tracking it:
```bash
git rm --cached filename    # remove from tracking without deleting the file
```

---

## SSH Setup for GitHub (one time)

SSH is more convenient and secure than typing your GitHub password.

```bash
# 1. Generate a key pair
ssh-keygen -t ed25519 -C "you@email.com"
# Hit enter to accept defaults → creates ~/.ssh/id_ed25519 (private) and id_ed25519.pub (public)

# 2. Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Copy the PUBLIC key
cat ~/.ssh/id_ed25519.pub   # copy the output

# 4. Add to GitHub: Settings → SSH and GPG Keys → New SSH Key → Paste

# 5. Test it
ssh -T git@github.com       # should say: Hi username! You've successfully authenticated...
```

Clone using SSH URLs from now on: `git@github.com:user/repo.git` (not `https://...`).

---

## Working with Remotes

```bash
git remote -v                       # show current remotes
git remote add origin URL           # add a remote
git remote set-url origin URL       # change remote URL (e.g., switch HTTPS → SSH)

git fetch origin                    # download remote changes, don't merge
git pull                            # fetch + merge
git pull --rebase                   # fetch + rebase (cleaner history)
git push                            # push current branch
git push -u origin feature/login    # push branch and set tracking (first time)
git push origin --delete feature/x  # delete remote branch
```

---

## Connecting a Local Repo to GitHub

**You have a local repo, want to put it on GitHub:**

```bash
# 1. Create a NEW empty repo on GitHub (no README — keep it blank)
# 2. Then:
git remote add origin git@github.com:yourusername/repo-name.git
git branch -M main
git push -u origin main
```

---

## The Feature Branch Workflow

Standard workflow for working with a team (or even solo on GitHub):

```bash
# 1. Start from an up-to-date main
git switch main
git pull

# 2. Create a feature branch
git switch -c feature/add-login

# 3. Work, commit often
git add .
git commit -m "Add login form"

# 4. Push to GitHub
git push -u origin feature/add-login

# 5. Open a Pull Request on GitHub
# → your branch page → "Compare & pull request" → write description → submit

# 6. After the PR is merged, clean up
git switch main
git pull
git branch -d feature/add-login
git push origin --delete feature/add-login
```

---

## Pull Requests (PRs)

A PR is a request to merge your branch into another branch (usually `main`). It's where code review happens on GitHub.

**Good PR habits:**
- Keep PRs small and focused — one thing per PR
- Write a clear title and body: what changed and why
- Reference issues: `Closes #42` auto-closes the issue on merge
- Review your own diff before submitting

**PR description template:**
```
## What
Brief description of the change.

## Why
Why this change is needed.

## How to test
Steps to verify it works.
```

---

## GitHub CLI (`gh`)

Lets you do GitHub things from the terminal:

```bash
# Install (macOS)
brew install gh

# Authenticate
gh auth login

# Repos
gh repo create my-repo --public
gh repo clone user/repo

# Pull Requests
gh pr create                   # create a PR (interactive)
gh pr list                     # list open PRs
gh pr checkout 42              # check out PR #42 locally
gh pr merge 42                 # merge a PR

# Issues
gh issue create
gh issue list
gh issue close 42

# CI/CD
gh run list                    # list workflow runs
gh run view 123456             # view details of a run
```

---

## Forking

Used when you want to contribute to a project you don't own:

```bash
# 1. Fork on GitHub (click the Fork button)
# 2. Clone your fork
git clone git@github.com:yourusername/forked-repo.git

# 3. Add the original as "upstream"
git remote add upstream git@github.com:originalowner/repo.git

# 4. Keep your fork in sync
git fetch upstream
git switch main
git merge upstream/main
git push
```

---

## Emergency Recovery: `git reflog`

`reflog` records every HEAD movement, including after resets. It's Git's hidden safety net.

```bash
git reflog                     # see recent HEAD history with hashes
git reset --hard abc1234       # restore to any entry in reflog
```

If you think you've lost commits with `reset --hard`, check reflog first — commits aren't actually deleted immediately.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Committed to `main` by accident | `git reset HEAD~1`, create correct branch, re-commit there |
| Committed a `.env` or secret | Rotate the secret immediately. Remove from history with `git filter-repo` or BFG. Deleting the file is not enough — history is public. |
| `git add .` included junk | Use `git add -p` next time to review changes before staging |
| Merge conflict | Edit the conflicting file to resolve markers, then `git add` + `git commit` |
| Force-pushed to shared branch | Don't. Use `git push --force-with-lease` — it fails if someone else pushed |
| PR has conflicts with main | `git switch your-branch`, `git pull --rebase origin main`, fix conflicts, push |
| Cloned with HTTPS, want SSH | `git remote set-url origin git@github.com:user/repo.git` |

---

## Quick Reference Card

```bash
# Start of day
git pull

# New feature
git switch -c feature/thing
git add . && git commit -m "..."
git push -u origin feature/thing
gh pr create

# Keep branch up to date with main
git fetch origin
git rebase origin/main

# After PR is merged
git switch main && git pull
git branch -d feature/thing
git push origin --delete feature/thing

# Oops recovery
git restore filename.py        # discard unstaged edit
git restore --staged file      # unstage
git reset HEAD~1               # undo last commit (keep work)
git reflog                     # find lost commits
```
