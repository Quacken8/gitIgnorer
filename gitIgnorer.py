import os
import pathspec


GITIGNORE = ".gitignore"

# find .gitignore and its contents
gitignoreLines = []
try:
    with open(GITIGNORE, "r") as f:
        gitignore = f.readlines()
except FileNotFoundError:
    print("No .gitignore file found")
    exit(1)

spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignoreLines)


# find all files in the directory
allPaths = []
for root, dirs, files in os.walk("."):
    for name in files:
        allPaths.append(os.path.join(root, name))

# compare the two

toBeDeleted = []
for path in allPaths:
    if spec.match_file(path):
        toBeDeleted.append(path)

# prompt delete
print("Found the following files to be deleted:")
for path in toBeDeleted:
    print(path)

delete = input("Delete? (y/n): ")

if delete == "y":
    for path in toBeDeleted:
        os.remove(path)