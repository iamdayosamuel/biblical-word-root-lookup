---
name: biblical-word-root-lookup
description: Default skill for Bible study questions. Looks up the Hebrew (OT) or Greek (NT) words behind a verse, passage, English word or Strong's number (H1 to H8674, G1 to G5624) and returns the Strong's definition, KJV renderings, root chain, same-root words and, for Hebrew, the entry number in Jeff A. Benner's Lexicon of Biblical Hebrew with the ancient letter pictures, so the user can read the ancient meaning in their printed copy. Saves each word study as its own Markdown note in the user's own words and layout. Use it first for any question about what a Bible word, verse or passage means, its original language, root, etymology, ancient Hebrew perspective or word study, even when Benner or Strong's is not named, and to save, review or search past word studies. Skip it only if the user says not to use it.
---

# Biblical Word Root Lookup

Strong's first (standard sense, KJV usage, root chain), then Benner's for the ancient picture-letter meaning. Benner's Lexicon is numbered by entry in the left margin and arranged by ancient parent root. The back of the book has a Strong's to Benner's index. This skill does that lookup instantly, so the user opens the book at the right entry.

Everything runs offline from the bundled files. No web call is needed for number lookups. The user is expected to own Benner's Lexicon of Biblical Hebrew. The skill gives the entry number and the letter pictures. The entry text stays in the book.

## Bundled data

- `references/strongs-hebrew.json`: 8,674 Hebrew Strong's entries.
- `references/strongs-greek.json`: 5,523 Greek Strong's entries (G1 to G5624, with Strong's own gaps).
- `references/strongs-to-benner.csv`: Strong's to Benner's table from the Lexicon index (pp. 526 to 558). Columns `strongs`, `benner`, `table_pages`. Hebrew only. One Strong's number can map to several Benner's entries.
- `references/ancient-alphabet.md`: Benner's table of the 22 ancient letters (picture, meaning, sound).
- `references/benner-entry-guide.md`: how to read a Benner's entry (parent, child, adopted roots, abbreviations).
- `references/study-note-format.md`: study settings, the three note layouts, and the rules for a study note.
- `references/SOURCES.md`: licences, attribution, known low-confidence rows.
- `scripts/lookup.py`: the lookup. `scripts/study_log.py`: makes and finds study notes.

## First use: setup questions

The first time the skill runs, before any lookup, check for a `Study-Settings.md` the user has pointed to or that sits in the working folder. If none exists, ask all of these together, once, as a short numbered list. Let the user answer in one line, and accept "defaults" for the rest:

1. **Which AI app are you using?** Claude Code, Claude.ai or the desktop app, ChatGPT, another assistant. This decides whether notes can be written straight to a folder (apps with a file system, such as Claude Code) or must appear in the chat for the user to paste into their own file (chat apps).
2. **Which app do you keep notes in?** Obsidian, another Markdown app, or just a folder. Obsidian means the `obsidian` layout. Anything else starts as `plain`.
3. **Where should study notes be saved?** A folder path (inside their vault if they use Obsidian). Skip if the app cannot write files.
4. **How do you write dates?** Offer examples such as 11-Oct-2026, 2026-10-11, 11/10/2026. If they would rather not say, ask them to type today's date their usual way and match it. If they use Obsidian daily notes, ask how those are named, so a `[[date]]` link points to a real note.
5. **What should a note look like?** Offer `plain`, `obsidian`, or `custom` (they share two or three of their own study notes and the skill copies that layout). Step 2 usually settles this. Only ask if it is unclear. See `references/study-note-format.md`.
6. **Anything else to adjust?** Note naming, fields they always keep (status, tags, Related to), language for the notes.

Output is Markdown for everyone, unless the user asks for another format. Save the answers with `python3 -I scripts/study_log.py init --folder <dir> --date-style "<style>" --layout <layout> --ai-app "<app>" --note-app "<app>"`, or write `Study-Settings.md` by hand using `references/study-note-format.md`. For `custom`, follow the instructions there. Do not ask again once settings exist. If the user later says they changed app, date style or layout, update the settings file once. On a later visit, read the settings first and search the folder for the word before making a new note. If the user pastes a note into the chat, use that.

Do not rely on any assistant memory feature for this. The files are the record, so it works in any tool.

## Default for Bible questions

Treat this skill as the first step for any Bible question about meaning, not only for word lookups.

- **Verse or passage question** ("what does Psalm 1:2 mean", "explain Proverbs 10:8"): get the Hebrew or Greek words with the interlinear (Workflow step 1), pick the two to five words that carry the meaning, and run the lookup. Lead the answer with those words (Strong's number and sense, Benner number, letter pictures). Add commentary after, and label it as general commentary.
- **Doctrinal, historical or other Bible question with no single word at issue:** still check whether one key word would sharpen the answer. Say in one line which words you checked. If none matter, answer normally.
- **The user says not to use the skill:** do not use it.
- **Phone or small screen:** lead with the answer and the numbers. Offer the full study note afterwards.
- **Scripts cannot run** (code execution is off): say so, and read `references/strongs-to-benner.csv` and the JSON files directly for the numbers.

## Workflow

1. **Get the Strong's number.**
   - Number given (H539, G26, "Strong's 1897"): go to step 2. A bare number means Hebrew. Ask if it could be Greek.
   - Word given (English, Hebrew letters, Greek letters, transliteration): run `python3 -I scripts/lookup.py --find "<word>"`. Results mix H and G. When several senses are plausible (for example "father" gives H1, H2, G3962), show the top few and let the user choose. Do not guess silently between different words.
   - Verse given: fetch an interlinear page with WebFetch, such as `https://biblehub.com/interlinear/<book>/<chapter>-<verse>.htm`, and read the Strong's numbers (Old Testament gives H numbers, New Testament gives G numbers). If the user asked about the whole verse, list the words with number, gloss and Benner number in a compact table, and expand only the key words. Without web access, ask the user for the Strong's numbers or the words.

2. **Run the lookup.** `python3 -I scripts/lookup.py H539 G26` (several allowed). `--family N` shows more same-root words.

3. **Report.** For each word, in this order:
   - Strong's number, original-language word, transliteration.
   - **Benner's number** (Hebrew only), prominent, with the table page spread so the user can check it. List all numbers if there are several.
   - Strong's definition in one or two lines (trim the KJV list to the senses that matter).
   - Root: the chain from the script, and the root's Benner number when different.
   - Two to five same-root words worth knowing, with Benner numbers for Hebrew.
   - For Hebrew: one line pointing to what to look for in Benner's, the entry's parent root and its Act, Obj and Abs ideas (see `references/benner-entry-guide.md`). Always give the pictograph: each letter's picture and meaning from `references/ancient-alphabet.md`, labelled as the letters' meanings. Then ask the user to read the entry in their printed Benner's and bring back what it says. Their reading of the book is the authority, and the study note is built from it.

4. **Offer to save the study.** After a lookup, ask once whether to save it, and ask for the user's own meaning in their words. When the user states what they have learned, save it without asking again. Each study is its own note, never a shared log, because users reuse studies as separate ideas. One note can hold a few related words when they are one train of thought. Make the skeleton with `python3 -I scripts/study_log.py add --folder <dir> --title "..." --strongs H1818 H1826`, then write the user's wording into the note in their voice and layout (see `references/study-note-format.md`). Capture their picture of the word, the connections they draw and any reading of their own, kept separate from the lexicon's. Do not flatten it, and do not add reasoning of your own. A second visit to the same study goes in with `study_log.py revisit --title "..." --text "..."`. To find earlier studies, run `study_log.py list --folder <dir> [--search text]` (newest first).

## New Testament and Greek

Benner's Lexicon covers Hebrew only, so a Greek word has no Benner number. The route to the ancient view:

- Strong's names a Hebrew source for Greek loanwords and names (for example G3 Abaddon from H11). The script prints it, with that word's Benner number.
- For other Greek words, the Hebrew background is a judgement, not data. When an NT verse quotes the Old Testament, take the Hebrew word from the quoted OT verse. Otherwise ask the user which Hebrew word they have in mind, or offer candidates and label them "likely, not certain".
- The Septuagint (Greek Old Testament) is the usual evidence for a Greek word's Hebrew counterpart. It is not bundled.

## Things that go wrong, and what to do

- **No Benner row.** About a third of Hebrew Strong's numbers have none (mostly proper names, some derived forms). Say "no Benner row". If the root has one, offer the root's number as the way in and label it as the root's.
- **Several Benner numbers.** Report all (H155 gives 808 and 809).
- **"Root" has two meanings.** The script's chain follows Strong's own derivation ("from H6"). Benner's parent root is a different, ancient two-letter level that only the book shows. Do not claim a Benner parent root from memory. Point to the entry.
- **Transcription risk.** The Benner table was read from photos of the book. If the user reports a number that does not match the book, trust the book, correct the row in `references/strongs-to-benner.csv`, and say which row changed. Low-confidence rows are listed in `references/SOURCES.md`.
- **Aramaic.** Entries marked `[Aramaic]` correspond to a Hebrew word. Report both numbers when the derivation names the Hebrew counterpart.
- **Do not invent meanings.** Strong's wording comes from the data. The ancient meaning of a root belongs to Benner's entry text, which this skill does not bundle. Give the number and let the user read the entry. If they paste the entry, discuss it with them.
- **Do not fill in the user's meaning.** It is their own words.
- **Outside the data.** Anything not in the bundled files or the user's reading of Benner's, such as how Modern Hebrew uses a word, is general knowledge. Say so, mark it "likely, not certain", and keep it out of the study note unless the user adopts it.
- **Dictated input.** Users often dictate, so numbers and names can arrive garbled ("11818" for H1818, "Benas" for Benner's). Read the intended number back before looking it up. Hebrew numbers are H, Greek are G, and the two ranges overlap.

## Style

Short replies. Lead with the number. Dates in the style set in `Study-Settings.md`, read once, never re-checked against the user's files.
