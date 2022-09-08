#!/usr/bin/env python3
import argparse
import json

parser = argparse.ArgumentParser(description='Generate pretty picklist from JSON, optionally topic-first')
parser.add_argument("-t", "--topic-first", action='store_true', help="List topics, then changes without a topic")

changes_file = open('changes.json', 'r', encoding='utf-8')
changes_data = changes_file.readlines()

topics = set()
loose_changes = dict()
for line in changes_data:
    if not line.strip():
        continue
    parsed_line = json.loads(line)
    if 'id' in parsed_line:
        if parser.parse_args().topic_first and 'topic' in parsed_line:
            topics.add(parsed_line['topic'])
        else:
            project = parsed_line['project']
            if project not in loose_changes:
                loose_changes[project] = dict()
            loose_changes[project][parsed_line['number']] = parsed_line['subject']

print("#!/bin/bash\n\n# Abort early on error\n\nset -eE\n")

if parser.parse_args().topic_first:
    print("## Topics\n")
    for topic in sorted(topics):
        print("./vendor/lineage/build/tools/repopick.py -t {}".format(topic))
    print("")

for project in sorted(loose_changes):
    print("## Project: {}\n".format(project))
    for change in dict(sorted(loose_changes[project].items(), key=lambda item: item[0])):
        print("./vendor/lineage/build/tools/repopick.py {} # {}".format(change, loose_changes[project][change]))
    print("")
