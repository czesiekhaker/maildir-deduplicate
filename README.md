# maildir-deduplicate

This script parses the output of `fdupes` and helps get rid of the
duplicates in Maildirs. I wrote it out of frustration after learning
that
[maildir-deduplicate](https://github.com/kdeldycke/maildir-deduplicate)
does not handle Unicode correctly (at least did not when I used it).

## Requirements

- [fdupes](https://github.com/adrianlopezroche/fdupes) (in most distros'
  repositories)

## Options

- `-n`, `--dry-run` does not delete any files

## Notes

You should configure the script by modifying `conditions` dict at the
top of the file. Run the script to see suggestions of rules or read the
comments above the declaration.

Additionally, if there are more than 2 locations for a duplicate, the
script tries to remove dupes from `ARCHIVE_PREFIX` dir if the message is
found in one of `ARCHIVE_PREFIX`'s subfolders. This takes care of
duplicated archives, eg. file being in both `.Archive` and
`.Archive.2015` folders.

Make backups, use with caution, when in doubt - read the code.
