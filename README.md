### This is the newest version of my first folder cleaner!

## Folder cleaner v.1.1

# how to use?

0. Make sure you have python3 and pip installed
1. Download the repository 
2. Launch `pip install -e . ` in terminal in the repository you just downloaded 
3. Launch `clean-folder` + `full\folder\to\clean\path` in terminal

**warning1: do not launch this script in folders that may contain unpacked unexamined archives**

**warning2: overrights a file with the same name as one it's tying to move** 

# what does it do?
- sorts files into separate folders with respect to the extensions;
- renames everything with respect to the convention;
- unpacks archives;
- deletes empty folders;
- ignores unknown formats;

# changes:
- it's now *cleaner*, not *sorter*
- now installable as a package
- console script


# to do list:
- [x] make it delete *all* the empty folders including 'images', 'video', etc
- [ ] write an exception for the case, when moving an item to the folder causes "file already exists" issue 
- [ ] extend the known formats range
- [ ] minor fixes of the helping functions I made up, for the sake of universality 
- [ ] scanning an archive with the antivirus before unpacking

to be continued
