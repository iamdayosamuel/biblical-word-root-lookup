# Context pass

Use only when asked, or after offering. Triggers: the user asks what a word, verse or passage meant to its first readers, asks for the background, or asks how to read it in context. After a full word study you may offer it in one line ("Want the context for this passage?") and wait. Never run it unasked. Run it after the Strong's and Benner's step, so the lexicon facts come first.

Aim: help the user read the passage as its first audience would, whether they are a new believer or a trained scholar. Match depth to the user. Plain words for a beginner. Named sources and open questions for a scholar. Ask which if unclear.

## Vault check (first)

Search the user's study folder once: `python3 -I scripts/study_log.py list --folder <dir> --search <word or Strong's number>`. One call. Read at most the top two matches. If the folder is unknown or nothing matches, skip it and say nothing. If notes match, give one line ("You have a note: <title>") and keep the user's own reading separate from anything new. Never search beyond the study folder.

## The contexts

Cover the ones that apply. Skip any that add nothing for this passage. One to three lines each.

1. **Word and root.** The Hebrew or Greek word, its root, and Benner's picture reading where a Benner entry exists (from the bundled data and the user's printed copy). Check ancient-hebrew.org (Jeff Benner's Ancient Hebrew Research Center) if web access exists. Set it beside what an academic lexicon says (BDB, HALOT, TWOT, NIDOTTE; BDAG for Greek). Say which source says which.
2. **Historical context.** When and where the passage was written or set. The events, rulers, politics, and the audience's situation behind it. Note where dating is debated.
3. **Cultural context.** How people lived and thought: family, honour and shame, land, work, trade, law, worship, daily habits, and the assumptions the first readers shared and the text does not explain.
4. **Literary context.** The genre (law, narrative, poetry, proverb, prophecy, letter, apocalyptic) and how that genre worked in the ancient world. Where the passage sits in its book and what surrounds it. Structure, repeated words, wordplay, and whether the passage follows or breaks the usual pattern of its genre.
5. **Ancient Near Eastern and Second Temple parallels.** Where a real parallel exists: Egyptian wisdom (Amenemope, Ptahhotep), Mesopotamian law and epic (Hammurabi, Gilgamesh, Enuma Elish), Ugaritic and other West Semitic texts, Hittite treaties, Dead Sea Scrolls, Septuagint, Josephus, Philo, rabbinic sources. Name the text and the matching section. If no real parallel exists, say so. For New Testament passages, the Greco-Roman setting (patronage, household codes, imperial cult) belongs here.
6. **Theological context.** Where the passage sits in the Bible's larger storyline, what the rest of Scripture says on the theme, and how the New Testament uses or quotes it. Name where traditions read it differently. Do not choose a side for the user.
7. **Sources to check.** Named with enough detail to verify: author, title, year, publisher or journal, and a page or section only if you have seen it. Prefer sources reachable online. If you could not open one, write "not opened" and give it as a lead.

## Rules

- **Label every claim:** bundled data, the user's own reading of Benner's, a source opened this session (give it), or general knowledge (mark "likely, not certain").
- **Benner's reading is one view.** The picture-letter approach of Benner and the Ancient Hebrew Research Center is not the consensus of academic Hebrew lexicography, which works from comparative Semitic evidence and usage. Show it as "Benner's reading" beside the academic reading. Where they agree, say so. Where they differ, show both and let the user judge.
- **Never invent a citation.** If a search finds nothing, say what was searched and what was not found. Check author, title and year before quoting.
- **Do not force parallels.** Similar wording across cultures is not proof of borrowing. Use "parallel" for similar content. Use "dependence" only where named scholars argue it, and cite them.
- **Keep disputed points open.** Dating, authorship and interpretation are debated. Say "debated" and show the main positions in a line each.
- **Keep it short.** Short blocks, then sources. The user can ask for more on any one.
- **User's note.** Add nothing from this pass to a study note unless the user adopts it in their own words.
- **Optional focus.** If `Study-Settings.md` has a `context_focus` (for example "commerce and law", "women in the text", "kingship"), give that lens first and keep the others brief.

## Leads to verify (none opened when this skill was built)

Well-known starting points. Confirm each before relying on it.

- Egyptian wisdom: Miriam Lichtheim, *Ancient Egyptian Literature*, vols. 1 to 3 (University of California Press, 1973 to 1980). Amenemope is often compared with Proverbs 22:17 to 24:22.
- Mesopotamian law: Martha T. Roth, *Law Collections from Mesopotamia and Asia Minor*, 2nd ed. (Scholars Press, 1997).
- Texts in translation: James B. Pritchard (ed.), *Ancient Near Eastern Texts Relating to the Old Testament*, 3rd ed. (Princeton, 1969); William W. Hallo and K. Lawson Younger (eds.), *The Context of Scripture* (Brill, 1997 to 2002). Both under copyright.
- Background to the Old Testament: John H. Walton, *Ancient Near Eastern Thought and the Old Testament* (Baker Academic, 2006).
- Background to the New Testament: Craig S. Keener, *The IVP Bible Background Commentary: New Testament*, 2nd ed. (IVP Academic, 2014).
- Hebrew lexicons: Brown, Driver and Briggs (1906, public domain); Koehler and Baumgartner, *HALOT* (Brill, 1994 to 2000); Harris, Archer and Waltke (eds.), *TWOT* (Moody, 1980).
- Greek lexicon: Bauer, Danker, Arndt and Gingrich, *BDAG*, 3rd ed. (University of Chicago Press, 2000).
- Open collections: ORACC (cuneiform texts), Sefaria (Hebrew texts and translations), ancient-hebrew.org.
