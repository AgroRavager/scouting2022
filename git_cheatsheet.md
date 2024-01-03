#Git Cheatsheet

# Typical workflow
1) Switch to the main branch, if necessary
2) Clone/pull main to ensure you have the latest code
3) Create a new branch for your work (Branches are short lived)
4) Edit code as needed/Test
5) Commit changes to your branch
6) repeat 4,5 as needed
7) switch branches back to main
8) Pull to ensure you have the latest version of main
9) Switch branches back to your branch
10) Rebase your branch onto main (if main has changed - resolve any merge collisions)
11) Switch branches to main
12) merge your branch onto main
13) Resolve any merge collisions
	13.a) Commit if needed
14) push to the remote


# Creating a repo (you probably won't need this often)
"git init <repo name>"

# Cloning a repository
"git clone <url> <destination dir>

# Syncing to the latest version 
"git pull"

# Creating a new branch and switching to it
#  (to make changes - don't work directly in main)
"git checkout -b <branch name>"

# Switching to a branch 
"git checkout <existing branch>"

# Checking to see which files are modified 
"git status"

# Checking to see which branches exist
"git branch -a"

# Adding files to the changeset for commit 
"git add <filename>"

# Discarding changes 
"git restore <file>"
OR
"git checkout -- <file>"
OR 
"git reset --hard HEAD~<# changes to revert>

# Commiting added changes to the current branch
"git commit -m <commit note>" 

# to alter a previous unpushed commit at head 
"git commit --amend"

# rebasing branchs
"git rebase <branch to rebase onto>"

# merging changes ** may require another commit if there are merge conflicts **
"git merge <branch to merge in>"

# Checking the history of the repo/file
"git log"
OR
"git log <filename>"

# hunting down a specific change owner
"git blame <filename>"

# Seeing what changes were made (good practice before merging) 

# pre commit
"git diff"

# post commit
"git diff <old commit id > <new commit id>"

# pushing changes
"git push"

