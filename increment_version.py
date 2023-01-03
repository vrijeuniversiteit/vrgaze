import os
import re


def increment_version():
	path = 'vrgaze/__init__.py'
	if not os.path.exists(path):
		print('File does not exist')

	# with open(path, "r") as f:
	# 	text = f.read()
	# pattern = re.compile(r"(\d+\.\d+\.\d+)")
	# match = pattern.search(text)
	# version = match.group(1)
	# major, minor, patch = map(int, version.split("."))
	# patch += 1
	# new_version = f"{major}.{minor}.{patch}"
	# text = pattern.sub(new_version, text)
	# with open(path, "w") as f:
	# 	f.write(text)
	#
	# print(f"Bumped version from {version} to {new_version}")


def main():
	increment_version()


if __name__ == "__main__":
	main()
