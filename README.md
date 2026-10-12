# Biblical Word Root Lookup

A Claude skill for Bible word studies. Give it an English word, a Hebrew or Greek word, a transliteration, a Strong's number or a verse. It returns the Strong's number and definition, the root chain, same-root words, and for Hebrew words the entry number in Jeff A. Benner's *Lexicon of Biblical Hebrew*. Open your printed Benner's at that number and read the ancient picture-letter meaning next to Strong's. Then save the study as its own Markdown note, in your words.

It does not replace the book. It removes the page flipping.

## What you get

- Strong's Hebrew (H1 to H8674) and Greek (G1 to G5624), bundled and offline.
- Benner's entry number for each Hebrew word, with the page spread of the index in the book so you can check it.
- Root chain from Strong's own derivation, plus other words from the same root.
- The ancient Hebrew letter pictures (Benner's alphabet table) for the word's letters.
- For Greek loanwords and names, the Hebrew source Strong's names, with its Benner number.
- An optional context pass, on request: word and root, historical, cultural, literary, Near Eastern and theological context, with named sources to verify. Claims are labelled by source, and Benner's picture reading is shown beside academic lexicons.
- One Markdown note per study. Three layouts: `plain` (any Markdown app), `obsidian` (wiki links, Related to and status fields), or `custom` (the skill copies the layout of your own notes). Dates in whatever style you write them.

## Example

Ask: "Strong's and Benner number for blood in Hebrew". The skill runs its lookup script and answers from this output:

```
H1818  דָּם  dâm (dawm)
  Benner 740 (table pp. 530-531)
  Strong's: blood (as that which when shed causes death) of man or an animal; by analogy,
            the juice of the grape; figuratively (especially in the plural) bloodshed
  Root chain: H1818 dâm <- H1826 dâmam  [primitive root]
  Root H1826: Benner 741 (table pp. 530-531)
  Same root H1826:
    H1748 דּוּמָם dûwmâm: still, silently          | Benner 743
    H1827 דְּמָמָה dᵉmâmâh: quiet, calm, silence  | Benner 742
```

Open your printed Benner's at entry 740, read it, and tell the skill what you found. It then saves a study note. The skill makes the skeleton (the `plain` layout is shown). The words under it are yours:

```
---
created: 2026-10-12T00:32
updated: 2026-10-12T00:32
---
# What does damim have to do with blood and money

Date: 12-Oct-2026

---

דָּם dâm - strong's 1818
Benner's Lexicon - 740
strong's: blood (as that which when shed causes death) of man or an animal...

(your own words: what the entry says, the letter pictures, the connections you see)
```

## Install

**Claude Code.** Copy the `biblical-word-root-lookup` folder into `~/.claude/skills/` (all projects) or `<project>/.claude/skills/` (one project). It must be an unzipped folder with `SKILL.md` inside. Restart Claude Code from that project.

**Claude.ai or the desktop app.** Download `biblical-word-root-lookup.skill` from the Releases page and upload it under Settings, Capabilities, Skills. Chats cannot write to your computer, so notes appear in the reply for you to paste into your own file.

**Other assistants.** The folder is plain Markdown, JSON, CSV and two Python scripts. Any tool that can read files and run Python 3 can use it. Others can paste `SKILL.md` as instructions.

Needs Python 3.8 or later. No packages.

## Use

Say things like:

- "Strong's number and Benner number for shalom"
- "Hebrew behind 'meditate' in Joshua 1:8"
- "H1818"
- "Root of agape"

On first use it asks which AI app and note app you use (for example Claude Code and Obsidian), where to save notes, how you write dates and which note layout you want, then remembers the answers in `Study-Settings.md`. After a lookup it asks you to read the entry in your own Benner's and bring back what it says. Your reading is the authority. The skill never writes your meaning for you.

You can also run the scripts directly:

```
python3 scripts/lookup.py H1897 G26
python3 scripts/lookup.py --find shalom --find ἀγάπη
python3 scripts/study_log.py init --folder ~/Bible-Notes --date-style "D-Mon-YYYY" --layout plain
python3 scripts/study_log.py add --folder ~/Bible-Notes --title "What does damim have to do with blood and money" --strongs H1818 H1826
python3 scripts/study_log.py list --folder ~/Bible-Notes --search blood
```

## Limits

- You need your own copy of Benner's *Lexicon of Biblical Hebrew*. The skill gives numbers and letter pictures. It does not include Benner's entry text.
- Benner's covers Hebrew only. Greek words have no Benner number. The Hebrew background of a Greek word is a judgement, and the skill labels it that way.
- About a third of Hebrew Strong's numbers have no row in Benner's index (mostly proper names).
- The Strong's to Benner's table was transcribed from photos of the book's index. It was spot-checked, not proofread row by row. Rows the transcriber was least sure of are listed in `references/SOURCES.md`. If a number does not match your book, trust the book and open an issue or a pull request with the row.
- Verse lookups need web access (a BibleHub interlinear page) to find the Strong's numbers for each word.

## Data and licences

- Code (`scripts/`): MIT, see `LICENSE`.
- Strong's Hebrew and Greek data: Open Scriptures, CC-BY-SA. Strong's text is public domain. Share-alike applies to the JSON files and any changes to them.
- Benner's table and alphabet pages: from *Benner's Lexicon of Biblical Hebrew* by Jeff A. Benner. The book's copyright notice allows copying for educational purposes without prior permission. Use this project for education and credit the book. This project is not affiliated with or endorsed by Jeff A. Benner or the Ancient Hebrew Research Center. Buy the book: it is the actual reference.

Full attribution is in `biblical-word-root-lookup/references/SOURCES.md`.

## Corrections welcome

Wrong Benner number, a missing Strong's match, a layout you want added: open an issue or a pull request. Edit `references/strongs-to-benner.csv` for number fixes and say which page you checked.
