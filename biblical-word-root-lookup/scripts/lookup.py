#!/usr/bin/env python3
"""Biblical word lookup: Strong's entry (Hebrew or Greek), root chain, word family,
and the Benner's Lexicon entry number (Hebrew words only).

Usage:
  lookup.py H539 G26 1897      Strong's numbers. A bare number means Hebrew.
  lookup.py --find father      search English gloss, transliteration, Hebrew or Greek letters
  lookup.py --find אמן         Hebrew letters (points ignored)
  lookup.py --find ἀγάπη       Greek letters (accents ignored)
  lookup.py H539 --family 40   show up to 40 family members (default 20)

Data lives in ../references: strongs-hebrew.json, strongs-greek.json, strongs-to-benner.csv.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and choke on Hebrew/Greek

REF = Path(__file__).resolve().parent.parent / "references"
HEB_POINTS = re.compile(r"[֑-ׇ]")
FIELDS = ("lemma", "xlit", "pron", "derivation", "strongs_def", "kjv_def")


def load():
    entries = {}
    for fname in ("strongs-hebrew.json", "strongs-greek.json"):
        with open(REF / fname, encoding="utf-8") as f:
            entries.update(json.load(f))
    for e in entries.values():  # a few source entries omit fields
        for k in FIELDS:
            e.setdefault(k, "")
    benner, pages = {}, {}
    with open(REF / "strongs-to-benner.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = "H" + row["strongs"]
            benner.setdefault(key, []).append(int(row["benner"]))
            pages.setdefault(key, row["table_pages"])
    return entries, benner, pages


def refs(derivation):
    """Strong's keys (H### or G###) named as the source of a word, ignoring 'Compare ...' notes."""
    head = re.split(r"\bCompare\b", derivation)[0]
    return [f"{m[0]}{int(m[1:])}" for m in re.findall(r"\b([HG]\d+)", head)]


def root_of(key, entries):
    """Follow the derivation chain within the same language. Returns (chain, how_it_ended)."""
    lang = key[0]
    chain, seen = [key], {key}
    while True:
        e = entries.get(chain[-1])
        if e is None:
            return chain, "missing entry"
        if re.search(r"primitive root|primary (word|verb|particle|preposition)|primary", e["derivation"]):
            return chain, "primitive root"
        nxt = [r for r in refs(e["derivation"]) if r[0] == lang and r not in seen and r in entries]
        if not nxt:
            return chain, "no further Strong's source"
        chain.append(nxt[0])
        seen.add(nxt[0])


def latin(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[ʼʻ'`]", "", s).lower()


def simplify(s):
    """Hebrew Strong's spells vowels as ow, uw, iy, ay. Drop the glide so 'shalom' matches 'shalowm'."""
    return re.sub(r"(?<=[aeiou])[wy]", "", s)


def fmt_benner(key, benner, pages):
    if key[0] == "G":
        return ""
    if key in benner:
        nums = ", ".join(str(b) for b in benner[key])
        return f"Benner {nums} (table pp. {pages[key]})"
    return "no Benner row"


def short(e, width=70):
    text = (e["strongs_def"] + " " + e["kjv_def"]).strip()
    return text if len(text) <= width else text[: width - 1].rstrip() + "…"


def label(key, e):
    pron = f" ({e['pron']})" if e["pron"] else ""
    return f"{key}  {e['lemma']}  {e['xlit']}{pron}"


def show(key, entries, benner, pages, family_limit):
    e = entries.get(key)
    if e is None:
        print(f"{key}: not in Strong's (Hebrew H1 to H8674, Greek G1 to G5624)\n")
        return
    aramaic = " [Aramaic]" if "Aramaic" in e["derivation"] else ""
    print(label(key, e) + aramaic)
    print(f"  {fmt_benner(key, benner, pages) or 'Greek: no Benner entry (Benner covers Hebrew only)'}")
    print(f"  Strong's: {e['strongs_def']}")
    print(f"  KJV: {e['kjv_def']}")
    print(f"  Derivation: {e['derivation']}")
    chain, how = root_of(key, entries)
    root = chain[-1]
    path = " <- ".join(f"{c} {entries[c]['xlit']}" for c in chain)
    print(f"  Root chain: {path}  [{how}]")
    if key[0] == "G":
        heb = [r for r in refs(e["derivation"]) if r[0] == "H" and r in entries]
        for h in heb:
            he = entries[h]
            print(f"  Strong's names Hebrew source {h} {he['lemma']} {he['xlit']}: {fmt_benner(h, benner, pages)}")
    if root != key:
        if fmt_benner(root, benner, pages):
            print(f"  Root {root}: {fmt_benner(root, benner, pages)}")
        if key[0] == "H" and key not in benner and root in benner:
            print("  Note: no Benner row for this number, so use the root's number as the way in.")
    lang = key[0]
    family = [
        m for m in entries
        if m[0] == lang and m != key and root_of(m, entries)[0][-1] == root
    ]
    family.sort(key=lambda m: int(m[1:]))
    if family:
        print(f"  Same root {root} ({len(family)} other words):")
        for m in family[:family_limit]:
            fe = entries[m]
            print(f"    {m} {fe['lemma']} {fe['xlit']}: {short(fe)}" + (f" | {fmt_benner(m, benner, pages)}" if m[0] == "H" else ""))
        if len(family) > family_limit:
            print(f"    … {len(family) - family_limit} more (use --family N)")
    print()


def find(query, entries, benner, pages, limit=15):
    q = query.strip()
    hebrew = bool(re.search(r"[א-ת]", q))
    greek = bool(re.search(r"[Ͱ-Ͽἀ-῿]", q))
    scored = []
    for key, e in entries.items():
        n = int(key[1:])
        score = 0
        if hebrew or greek:
            if hebrew and key[0] != "H" or greek and key[0] != "G":
                continue
            if hebrew:
                qs, lem = HEB_POINTS.sub("", q), HEB_POINTS.sub("", e["lemma"])
            else:
                qs, lem = latin(q), latin(e["lemma"])
            if lem == qs:
                score = 100
            elif qs in lem:
                score = 40
        else:
            ql = latin(q)
            xl = latin(e["xlit"])
            qx = ql
            if key[0] == "H":
                xl, qx = simplify(xl), simplify(ql)
            pat = re.compile(r"\b" + re.escape(ql) + r"\b", re.I)
            lead = e["strongs_def"].lower().lstrip("{ ")
            if xl == qx:
                score = 100
            elif lead.startswith(ql) and pat.search(lead[: len(ql) + 1]):
                score = 90
            elif pat.search(e["kjv_def"]) and e["kjv_def"].lower().startswith(ql):
                score = 70
            elif pat.search(e["strongs_def"]):
                score = 60
            elif pat.search(e["kjv_def"]):
                score = 50
            elif qx in xl:
                score = 30
        if score:
            scored.append((-score, key[0] != "H", n, key))
    scored.sort()
    if not scored:
        print(f"No match for {query!r}. Try a root word, a transliteration, or a KJV rendering.")
        return
    print(f"{len(scored)} match(es) for {query!r}, best first (H = Hebrew, G = Greek):")
    for _, _, _, key in scored[:limit]:
        e = entries[key]
        print(f"  {key} {e['lemma']} {e['xlit']}: {short(e)}" + (f" | {fmt_benner(key, benner, pages)}" if key[0] == "H" else ""))
    if len(scored) > limit:
        print(f"  … {len(scored) - limit} more. Narrow the query or look up numbers directly.")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("numbers", nargs="*", help="Strong's numbers, e.g. H539, G26 or 539 (Hebrew)")
    ap.add_argument("--find", action="append", default=[], help="search text; repeatable")
    ap.add_argument("--family", type=int, default=20, help="max same-root words to list")
    a = ap.parse_args()
    if not a.numbers and not a.find:
        ap.print_help()
        sys.exit(1)
    entries, benner, pages = load()
    for q in a.find:
        find(q, entries, benner, pages)
    for raw in a.numbers:
        m = re.fullmatch(r"([HhGg]?)(\d+)", raw.strip())
        if not m:
            print(f"Skipping {raw!r}: not a Strong's number. Use --find for words.\n")
            continue
        lang = (m.group(1) or "H").upper()
        show(f"{lang}{int(m.group(2))}", entries, benner, pages, a.family)


if __name__ == "__main__":
    main()
