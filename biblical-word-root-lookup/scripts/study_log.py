#!/usr/bin/env python3
"""Keep Bible word studies as separate Markdown notes, one note per study.

A study can cover one word or several related words. The script makes the note skeleton
(frontmatter, title, date, one block per Strong's number with its Benner number). The
user's own words and thinking are added to the note afterwards. Where the assistant cannot
run scripts, write the same Markdown by hand (format in ../references/study-log-format.md).

Usage:
  study_log.py init    --folder DIR [--date-style "D-Mon-YYYY"] [--layout plain|obsidian|custom]
                       [--ai-app "Claude Code"] [--note-app Obsidian]
  study_log.py add     --folder DIR --title "Note title" --strongs H1818 [H3701 ...]
  study_log.py revisit --folder DIR --title "Note title" --text "What I saw this time"
  study_log.py list    --folder DIR [--search TEXT]

Files written inside DIR:
  Study-Settings.md   date style and layout (read on every later run)
  <Note title>.md     one note per study

Date style tokens: YYYY, MM, DD (02), D (2, no leading zero), Mon (Oct), Month (October).
"D-Mon-YYYY" gives 12-Oct-2026 and 7-Oct-2026.

Layouts:
  plain     frontmatter, "# Title", "Date: ...", no wiki links. Works in any Markdown app.
  obsidian  adds Related to / status fields, [[wiki links]] on the title and date, and a
            [[Benner's Lexicon of Biblical Hebrew|Benners]] link.
  custom    the user's own layout, copied from their notes. The script writes the plain
            skeleton and the assistant reshapes it to match.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lookup  # noqa: E402

SETTINGS = "Study-Settings.md"
ILLEGAL = re.compile(r'[*"\\/<>:|?]')
LAYOUTS = ("plain", "obsidian", "custom")


def fmt_date(style, d=None):
    d = d or dt.date.today()
    parts = {"Month": d.strftime("%B"), "Mon": d.strftime("%b"), "YYYY": str(d.year),
             "MM": f"{d.month:02d}", "DD": f"{d.day:02d}", "D": str(d.day)}
    return re.sub(r"Month|Mon|YYYY|MM|DD|D", lambda m: parts[m.group(0)], style)


def stamp():
    return dt.datetime.now().strftime("%Y-%m-%dT%H:%M")


def read_settings(folder):
    path = folder / SETTINGS
    if not path.exists():
        sys.exit(f"No {SETTINGS} in {folder}. Run: study_log.py init --folder {folder}")
    cfg = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"-\s*([a-z_]+):\s*(.*)", line)
        if m:
            cfg[m.group(1)] = m.group(2).strip()
    cfg.setdefault("date_style", "D-Mon-YYYY")
    cfg.setdefault("layout", "plain")
    return cfg


def note_path(folder, title):
    name = ILLEGAL.sub("", title).strip().rstrip(".")
    if not name:
        sys.exit("The title has nothing usable left once illegal filename characters are removed.")
    return folder / f"{name}.md"


def date_line(cfg):
    today = fmt_date(cfg["date_style"])
    return f"[[{today}]]" if cfg["layout"] == "obsidian" else f"Date: {today}"


def init(a):
    folder = Path(a.folder).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / SETTINGS).write_text(
        f"---\ncreated: {stamp()}\n---\n# Study settings\n\n"
        f"- date_style: {a.date_style}\n- layout: {a.layout}\n"
        + (f"- ai_app: {a.ai_app}\n" if a.ai_app else "")
        + (f"- note_app: {a.note_app}\n" if a.note_app else "")
        + "- format: one Markdown note per study\n",
        encoding="utf-8",
    )
    print(f"Ready: {folder / SETTINGS}")


def word_block(key, entries, benner, layout):
    e = entries.get(key)
    if e is None:
        sys.exit(f"{key} is not in Strong's.")
    lines = [f"{e['lemma']} {e['xlit']} - strong's {int(key[1:])}" + ("" if key[0] == "H" else " (Greek)")]
    if key[0] == "H":
        nums = " and ".join(str(n) for n in benner.get(key, [])) or "no Benner row"
        link = "[[Benner's Lexicon of Biblical Hebrew|Benners]]" if layout == "obsidian" else "Benner's Lexicon"
        lines.append(f"{link} - {nums}")
    lines.append(f"strong's: {e['strongs_def']}")
    return "\n".join(lines)


def add(a):
    folder = Path(a.folder).expanduser()
    cfg = read_settings(folder)
    path = note_path(folder, a.title)
    if path.exists():
        sys.exit(f"{path.name} already exists. Use revisit to add to it, or choose another title.")
    entries, benner, _ = lookup.load()
    blocks = []
    for raw in a.strongs:
        m = re.fullmatch(r"([HhGg]?)(\d+)", raw.strip())
        if not m:
            sys.exit(f"{raw!r} is not a Strong's number. Use H1818 or G26.")
        key = f"{(m.group(1) or 'H').upper()}{int(m.group(2))}"
        blocks.append(word_block(key, entries, benner, cfg["layout"]))
    title = path.stem
    if cfg["layout"] == "obsidian":
        head = f"---\ncreated: {stamp()}\nupdated: {stamp()}\nRelated to:\nstatus:\n---\n# [[{title}]]\n"
    else:
        head = f"---\ncreated: {stamp()}\nupdated: {stamp()}\n---\n# {title}\n"
    path.write_text(head + f"\n{date_line(cfg)}\n\n---\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"Created {path}")


def revisit(a):
    folder = Path(a.folder).expanduser()
    cfg = read_settings(folder)
    path = note_path(folder, a.title)
    if not path.exists():
        sys.exit(f"{path.name} does not exist. Use add first.")
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^updated:.*$", f"updated: {stamp()}", text, count=1)
    text = text.rstrip("\n") + f"\n\n---\n\n{date_line(cfg)}\n\n{a.text}\n"
    path.write_text(text, encoding="utf-8")
    print(f"Added a dated section to {path.name}")


def list_(a):
    folder = Path(a.folder).expanduser()
    read_settings(folder)
    norm = lambda t: lookup.simplify(lookup.latin(t))
    notes = sorted((p for p in folder.glob("*.md") if p.name != SETTINGS),
                   key=lambda p: p.stat().st_mtime, reverse=True)  # newest first
    shown = 0
    for p in notes:
        body = p.read_text(encoding="utf-8")
        if a.search and norm(a.search) not in norm(p.stem + " " + body):
            continue
        strongs = ", ".join(sorted(set(re.findall(r"strong's (\d+)", body))))
        print(f"{p.stem}" + (f"  (strong's {strongs})" if strongs else ""))
        shown += 1
    print(f"{shown} of {len(notes)} notes.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--folder", required=True)
    p.add_argument("--date-style", default="D-Mon-YYYY")
    p.add_argument("--layout", default="plain", choices=LAYOUTS)
    p.add_argument("--ai-app", default="")
    p.add_argument("--note-app", default="")
    p.set_defaults(fn=init)
    p = sub.add_parser("add")
    p.add_argument("--folder", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--strongs", required=True, nargs="+")
    p.set_defaults(fn=add)
    p = sub.add_parser("revisit")
    p.add_argument("--folder", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--text", required=True)
    p.set_defaults(fn=revisit)
    p = sub.add_parser("list")
    p.add_argument("--folder", required=True)
    p.add_argument("--search", default="")
    p.set_defaults(fn=list_)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
