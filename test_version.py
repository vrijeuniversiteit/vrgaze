import re
import subprocess

with open("setup.py", "r") as f:
	text = f.read()
	pattern = re.compile(r"(\d+\.\d+\.\d+)")
	match = pattern.search(text)
	current_version = match.group(1)

last_commit_version = subprocess.run(
	["git", "show", "HEAD:setup.py"],
	stdout=subprocess.PIPE,
	encoding="utf-8",
).stdout

pattern = re.compile(r"(\d+\.\d+\.\d+)")
match = pattern.search(last_commit_version)
last_commit_version = match.group(1)

if current_version == last_commit_version:
	exit(1)  # no new version, bad exit
else:
	exit(0)
