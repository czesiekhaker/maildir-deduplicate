#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import json
import os
import re
from optparse import OptionParser

# hacks:
# ./maildir-dedup.py -n | grep '): N,' | sort | uniq

# where to expect fdupes results
fdupes_path = "fdupes.out"

decisions = {
    # 0: remove the first, keep the second
    # 1: remove the second, keep the first
    # eg. ("first_dir", "second_dir"): 1,
    # will remove second_dir

    # put rules here
}

ARCHIVE_PREFIX = "Maildir/.Archives"

parser = OptionParser()
parser.add_option("-n", "--dry-run", action="store_true", default=False)
(options, args) = parser.parse_args()

def remove_file(path):
    print "  removing", path
    if not options.dry_run and os.path.isfile(path):
        os.remove(path)

if not os.path.isfile(fdupes_path):
    print "File", fdupes_path, "not found, run `fdupes --recurse --noempty --sameline Maildir > fdupes.out` manually first"
    exit(1)

# add reverse entries so that there's no need to manually add them
decisions_reversed = {}
for pair, decision in decisions.items():
    decisions_reversed[(pair[1], pair[0])] = (decision + 1) % 2
decisions.update(decisions_reversed)

for pair, decision in decisions.items():
    if decision:
        print "→ favouring", pair[0], "over", pair[1]
print ""

with open(fdupes_path) as f:
    for line in f:
        # split on unescaped spaces
        paths = re.split(r'(?<!\\) ', line.rstrip())
        # remove espacing on spaces
        paths = [path.replace('\ ', ' ') for path in paths]

        paths_str = json.dumps(paths)
        print paths_str

        # skip these filenames
        first_filename = os.path.basename(paths[0])
        if first_filename in ['dovecot-keywords']:
            print "  skipping", first_filename, "(on the naughty list)"
            continue


        # in more than 2 places
        if len(paths) > 2:
            # if in .Archives and .Archives.sth delete the former
            arch_cnt = 0
            for path in paths:
                if path.startswith(ARCHIVE_PREFIX):
                    arch_cnt = arch_cnt + 1

            if arch_cnt > 1:
                for path in paths:
                    if path.startswith(ARCHIVE_PREFIX + '/cur/'):
                        remove_file(path)

            # otherwise do nothing
            print "  skipping", paths_str, "(in more than 2 places, not handled by ARCHIVE_PREFIX)"
            continue

        dirs = [ os.path.dirname(path) for path in paths ]

        if dirs[0] == dirs[1]:
            print "  duplicates in the same dir, deleting second one"
            remove_file(paths[1])

        else:
            if tuple(dirs) in decisions:
                to_delete = paths[decisions[tuple(dirs)]]
                remove_file(to_delete)

            else:
                dirs.sort()
                print "  add"
                print "    ('" + dirs[0] + "', '" + dirs[1] + "'): N,"
                print "  to decisions dict; N = 0|1"
