import pathlib
import sys

PATCHES = [
    {
        "marker": "if entry.lower() == _TEXMAKE_LISTS:",
        "old": (
            "        candidate = os.path.join(current, _TEXMAKE_LISTS)\n"
            "        if os.path.isfile(candidate):\n"
            "            return candidate\n"
        ),
        "new": (
            "        candidate = os.path.join(current, _TEXMAKE_LISTS)\n"
            "        if os.path.isfile(candidate):\n"
            "            return candidate\n"
            "        try:\n"
            "            for entry in os.listdir(current):\n"
            "                if entry.lower() == _TEXMAKE_LISTS:\n"
            "                    path = os.path.join(current, entry)\n"
            "                    if os.path.isfile(path):\n"
            "                        return path\n"
            "        except OSError:\n"
            "            pass\n"
        ),
    },
    {
        "marker": "or any parent directory\")\n        sys.exit(1)",
        "old": (
            "        print(f\":: No {_TEXMAKE_LISTS} found in '{startDir}' or any parent "
            "directory\")\n"
            "        sys.exit(0)\n"
        ),
        "new": (
            "        print(f\":: No {_TEXMAKE_LISTS} found in '{startDir}' or any parent "
            "directory\")\n"
            "        sys.exit(1)\n"
        ),
    },
]


def main(path):
    source = pathlib.Path(path)
    text = source.read_text(encoding="utf-8")
    changed = False
    for patch in PATCHES:
        if patch["marker"] in text:
            continue
        if patch["old"] not in text:
            print(
                "patch_texmake_case: expected block missing in "
                + str(path)
                + "; upstream texmake.py changed, update the patch",
                file=sys.stderr,
            )
            return 1
        text = text.replace(patch["old"], patch["new"], 1)
        changed = True
    if not changed:
        print("patch_texmake_case: " + str(path) + " already patched")
        return 0
    source.write_text(text, encoding="utf-8", newline="\n")
    print("patch_texmake_case: " + str(path) + " patched")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: patch_texmake_case.py <path to texmake.py>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
