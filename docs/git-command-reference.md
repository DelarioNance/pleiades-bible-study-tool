# 🧭 Git Command Reference

## 🔹 `git fetch`
**What it does:**  
Downloads new commits from the remote **without modifying your working directory or your local branches**.

**Use when:**  
You want the latest remote changes but don’t want to modify your branch yet.

---

## 🔹 `git merge`
**What it does:**  
Combines two branches by creating a **merge commit**.

**Key points:**
- Preserves full history  
- Creates a commit with two parents  
- Produces non‑linear history  
- No rewriting of commits  

**Use when:**  
Integrating finished work into `main`, or when you want to preserve the true historical timeline.

---

## 🔹 `git pull`
**What it does:**  
`git pull` = **fetch + merge**

**Key points:**
- Updates your branch and merges in remote changes  
- Can create unwanted merge commits  
- Modifies your working directory  

**Use when:**  
Updating `main` or another long‑lived branch where merge commits are acceptable.

---

## 🔹 `git rebase`
**What it does:**  
Replays your commits on top of another branch, **rewriting history**.

**Key points:**
- Produces clean, linear history  
- Should not be used on shared branches  

**Use when:**  
Updating a feature branch with the latest `main` before opening or updating a PR.
