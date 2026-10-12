# Study note format

Plain Markdown, so it works in any app and any assistant. One note per study, in the folder the user chose. There is no shared word log, because users reuse studies as separate ideas.

## Study-Settings.md

```
---
created: 2026-10-12T00:32
---
# Study settings

- date_style: D-Mon-YYYY
- layout: plain
- ai_app: Claude Code
- note_app: Obsidian
- format: one Markdown note per study
```

- `date_style` tokens: YYYY, MM, DD (02), D (2, no leading zero), Mon (Oct), Month (October). The user's own style, never imposed. It is the single source for the format. If the user changes how they write dates, update it once.
- `layout` is `plain`, `obsidian` or `custom` (below).
- `ai_app` and `note_app` record the answers to the first-run questions. If `ai_app` is a chat app with no file access, show notes in the reply for the user to paste.

## Layouts

**plain** (default, works anywhere)

```
---
created: 2026-04-16T19:18
updated: 2026-04-17T18:01
---
# Title in plain language

Date: 16-Apr-2026

---

כֹּחַ ko'akh - strong's 3581
Benner's Lexicon - 1612
strong's: strength, power, force
(the user's own words: what it means, the picture, what sits next to it in the book)

---

Date: 17-Apr-2026

(a later visit: the user's further thinking or application)
```

**obsidian** (wiki links and the fields Obsidian users tend to keep)

```
---
created: 2026-04-16T19:18
updated: 2026-04-17T18:01
Related to: "[[another study note]]"
status:
---
# [[Title in plain language]]

[[16-Apr-2026]]

---

כֹּחַ ko'akh - strong's 3581
[[Benner's Lexicon of Biblical Hebrew|Benners]] - 1612
strong's: strength, power, force
(the user's own words)
```

The `[[date]]` link only helps if the user's daily notes are named in that same style. Ask, or check one daily note, before using it.

**custom** (the user's own layout)

Ask the user to share two or three of their own study notes. Copy their structure: frontmatter fields, heading style, how they write the word and number line, where the Benner number goes, how they date later sections, how they link notes. Run `study_log.py add` for the plain skeleton, then reshape the file to match their notes. Save one of their notes as `Layout-Example.md` in the study folder and name it in `Study-Settings.md` (`layout_example: Layout-Example.md`), so later sessions copy the same layout.

## Rules for every layout

- One note per study. A study is one idea. It may cover a few related words when they are one train of thought, each in its own block.
- The title is a plain-language question or idea, never an acronym. No `* " \ / < > : | ?` in it. The `add` command makes the skeleton and checks the title.
- The body is the user's voice, in their own layout: word and Strong's number, then the Benner number, then their meaning, their picture of the letters, the connections they draw to other words and notes, neighbouring entries, applications.
- Keep the user's reading separate from the lexicon's. Label their own inferences ("my reading, not Benner's") so it stays clear which is which.
- A line the user gave nothing for is left out. Do not invent or tidy their thinking. Do not add tags.
- A later visit to the same study adds a new dated section at the bottom (`study_log.py revisit`), not a second note.
- Link related studies to each other when the layout supports links.
- Greek entries have no Benner line.

## Without a file system

In chat apps that cannot save files, show the note in a Markdown block at the end of the reply and say "paste this into a new note". When the user returns and pastes a note, read it and carry on from there.
