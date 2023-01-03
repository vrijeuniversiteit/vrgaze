# Contribute

## Creating pull request
To contribute to the repository, clone the repository from GitHub and create a fork.
```bash
git clone https://github.com/vrijeuniversiteit/vrgaze.git
cd vrgaze

git remote add fork https://github.com/my-user/my-fork.git
git push --set-upstream fork master

# Edit some files

# Add changes to the staging area
git add .
git commit -m "Add changes"
```

## Testing if project works
Run the following lines in the terminal to test if the project works:
```bash
pre-commit install
pre-commit run --all-files
```
After installing the pre-commit hook, the hook will also run automatically on each commit.

