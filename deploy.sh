#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Update post from til repository.
git submodule update --remote

# Build the project.
# hugo -t <your theme>
# hugo -t Book --gc --cleanDestinationDir

# Find and kill Hugo server processes
ps -ef | grep "hugo server" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null

# Build the project into temporary folder.
TMP_PUBLIC="public_tmp"
rm -rf "$TMP_PUBLIC"
hugo -t seotax --gc --destination "$TMP_PUBLIC"

# Sync into public but preserve .git
rsync -a --delete --exclude='.git' "$TMP_PUBLIC"/ public/
rm -rf "$TMP_PUBLIC"

# Go to public folder, submodule commit
cd public
# Add changes to git.
git add .

# Commit changes.
msg="rebuild: $(date +"%Y-%m-%dT%H:%M:%S%z")"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin source

# Come back up to the project root
cd ..

# Commit and push to main branch
git add .

if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

git push origin main