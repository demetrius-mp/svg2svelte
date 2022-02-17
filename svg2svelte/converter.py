import shutil
import xml.etree.ElementTree as et
from pathlib import Path


def dash_case_to_pascal_case(name: str) -> str:
    return "".join(word.title() for word in name.split("-"))


def add_rest_props(file: Path):
    tree = et.parse(file)
    root = tree.getroot()
    root.attrib.pop("width")
    root.attrib.pop("height")

    xmlstring = et.tostring(root).decode("utf8")

    fixed_xmlstring = ""
    for i, line in enumerate(xmlstring.split("\n")):
        if i == 0:
            fixed_line = line.replace(":ns0", "", 1)
            fixed_line = fixed_line.replace("ns0:", "", 1)

            rest_props = " {...$$restProps}"
            fixed_line = fixed_line[:4] + rest_props + fixed_line[4:]

            fixed_xmlstring += fixed_line + "\n"
        else:
            fixed_xmlstring += line.replace("ns0:", "", 1) + "\n"

    with open(file, "w") as f:
        f.write(fixed_xmlstring)


def svg_to_svelte(in_folder: Path, out_folder: Path):
    if out_folder.exists():
        shutil.rmtree(out_folder)

    out_folder.mkdir(exist_ok=True)

    print("Copying files to output directory...")
    for file in in_folder.iterdir():
        shutil.copy(file, out_folder)

    print("Renaming and adding restProps...")
    for file in out_folder.iterdir():
        old_filename = file.stem
        new_filename = dash_case_to_pascal_case(old_filename) + "Icon.svelte"
        out_file = file.rename(out_folder / new_filename)

        add_rest_props(out_file)


if __name__ == "__main__":
    icon_type = "solid"
    in_folder = Path.cwd() / "icons" / icon_type
    out_folder = Path.cwd() / "svelte-icons" / icon_type

    svg_to_svelte(in_folder, out_folder)
    # add_rest_props(out_folder / "AdjustmentsIcon.svelte")
