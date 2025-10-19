#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Update post from til repository.
git submodule update --remote

# Build the project.
# hugo -t <your theme>
hugo -t Book

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