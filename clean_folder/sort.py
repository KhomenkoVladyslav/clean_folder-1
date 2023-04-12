from pathlib import Path
import re
import shutil
import sys


# ---------------------------GLOBALS ------------------------------


sorting_folders = ["images", "video", "documents", "audio", "archives"]

imgs = ("JPEG", "PNG", "JPG", "SVG")
vids = ("AVI", "MP4", "MOV", "MKV")
docs = ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX")
musc = ("MP3", "OGG", "WAV", "AMR")
arch = ("ZIP", "GZ", "TAR")

allowed_formats = imgs + vids + docs + musc + arch

sorting_formats = [imgs, vids, docs, musc, arch]

l_known = set()  # listing the known extentions
l_unknown = set()  # listing the unknown extentions
data = dict()  # dictionary with categories as keys and lists as values


# ---------------GET THE RIGHT FOLDER FOR THE EXTENTION --------------


dic_format_to_folder = {}
for i in range(len(sorting_formats)):
    dic_format_to_folder.update(
        {x.lower(): sorting_folders[i] for x in sorting_formats[i]}
    )


# ---------------STUFF FOR NORMILIZING NAMES ---------------------


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "h",
    "d",
    "e",
    "yo",
    "j",
    "z",
    "y",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)

TRANS = {ord(x): y for x, y in zip(CYRILLIC_SYMBOLS, TRANSLATION)}
big_letters = {ord(x.upper()): y.upper() for x, y in zip(CYRILLIC_SYMBOLS, TRANSLATION)}
TRANS.update(big_letters)


def normilize(string):
    """makes a word appropriate for file or folder naming"""

    return re.sub(r"[^a-zA-Z0-9]", "_", string.translate(TRANS))


# ---------------IGNORING SOME FOLDERS AND FILES ------------------


def is_file_upd(p):
    if p.is_file():
        if p.suffix.upper()[1:] in allowed_formats:
            return True
    return False


def is_dir_upd(p):
    if p.is_dir():
        if p.name not in sorting_folders:
            return True
    return False


# ---------------DATA COLLECTION ----------------------------------


def data_upd(key, what):
    """updates the dictionary with
    categories as keys and lists as values"""

    try:
        data[key].append(what)
    except:
        data.update({key: [what]})


def generate_table(dict):
    """takes a dictionary with the list values
    and prints a nice table"""

    n = 35
    print("|".join(rf"{i : ^35}" for i in dict.keys()))
    print("|".join("-" * n for i in dict.keys()))
    for k in range(len(max(dict.values(), key=len))):
        line = []
        for i in data.values():
            try:
                line.append(i[k])
            except:
                line.append(" ")
        print("|".join(rf"{i : ^35}" for i in line))
    print("|".join("-" * n for i in dict.keys()))


# ---------------MAIN ALGORITHM----------------------------------


def main(p):
    """takes a Path object as an input;
    collects data on the way while sorting files and folders"""

    for f in p.iterdir():
        if f.is_dir():
            try:
                f.rmdir()
            except OSError:
                if is_dir_upd(f):
                    name = normilize(f.stem)
                    data_upd("folders", name)

                    if f.stem != name:
                        f.rename(f"{current_parent}\{name}")
                    main(Path(f"{current_parent}\{name}"))

        elif is_file_upd(f):
            current_parent = f.parent
            name = normilize(f.stem)
            format = f.suffix[1:]
            target_folder = dic_format_to_folder.get(format)

            if format.upper() in arch:
                data_upd(target_folder, name)

                try:
                    shutil.unpack_archive(f, f"{current_parent}\{target_folder}\{name}")
                    f.unlink()
                except FileNotFoundError:
                    Path(f"{current_parent}\{target_folder}").mkdir()
                    Path(f"{current_parent}\{target_folder}\{name}").mkdir()
                    shutil.unpack_archive(f, f"{current_parent}\{target_folder}\{name}")
                    f.unlink()

            else:
                l_known.add(format.upper())
                data_upd(target_folder, f.name)

                try:
                    shutil.move(
                        f, f'{current_parent}\{target_folder}\{name+"."+format}'
                    )

                except FileNotFoundError:
                    Path(f"{current_parent}\{target_folder}").mkdir()
                    shutil.move(
                        f, f'{current_parent}\{target_folder}\{name+"."+format}'
                    )

        else:
            name = normilize(f.stem)
            current_parent = f.parent

            if f.is_file():
                data_upd("others", f"{name + f.suffix}")
                l_unknown.add(f.suffix[1:].upper())

                if f.stem != name:
                    f.rename(f"{current_parent}\{name + f.suffix}")


# --------- LAUNCHING THE SORTING AND REPORTING DATA -------------------------------------------


def launch():
    if len(sys.argv) == 2:
        try:
            p = Path(sys.argv[1])
            main(p)
            print("----------------------------------------------------------")
            print("the sorting is complete! here is some data report for you:")
            print("----------------------------------------------------------")
            generate_table(data)
            print(f"list of the known formats: {list(l_known)}")
            print(f"list of the unknown formats: {list(l_unknown)}")

        except:
            print("something went wrong! please check your path input")
    else:
        print("Please enter 'clean-folder *a directory to sort here*' ")
