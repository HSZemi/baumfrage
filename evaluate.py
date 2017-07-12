#! /usr/bin/env python3

import sys
import os
import json

keys = ["q1", "q2_fsem", "q2_lp", "q3", "q4", "q5-dependencies", "q5-failed-admission", "q5-failed-module", "q5-family", "q5-future", "q5-grade-improvement", "q5-job", "q5-long-project-group", "q5-minor-subject", "q5-modules-o-plenty", "q5-moved-module", "q5-other", "q5-pg2", "q5-planned", "q5-thesis-problems", "q6-dependencies", "q6-failed-admission", "q6-failed-module", "q6-family", "q6-future", "q6-grade-improvement", "q6-job", "q6-long-project-group", "q6-minor-subject", "q6-modules-o-plenty", "q6-moved-module", "q6-other", "q6-pg2", "q6-planned", "q6-thesis-problems", "q7", "q8", "timestamp", "userid"]

if len(sys.argv) < 2:
	print("usage: {} <path_with_json_data_files>".format(sys.argv[0]))
	sys.exit()

target_dir = sys.argv[1]

if not os.path.isdir(target_dir):
	print("Error: '{}' is not a directory.".format(target_dir))
	sys.exit()

for key in keys:
	print(key, end="\t")
	if key[:2] in ("q5","q6"):
		print("{}-extra".format(key), end="\t")
print("")

for filename in os.listdir(target_dir):
	fullpath = os.path.join(target_dir, filename)
	if os.path.isfile(fullpath) and fullpath[-5:] == ".json":
		with open(fullpath, "r") as f:
			data = json.load(f)
			for key in keys:
				if key[:2] in ("q5","q6"):
					if data[key[:2]][key]['checked'] == "true":
						print("true", end="\t")
					else:
						print("false", end="\t")
					if 'extra' in data[key[:2]][key]:
						print(data[key[:2]][key]['extra'], end="\t")
					else:
						print("", end="\t")
				else:
					print(data[key], end="\t")
			print("")


