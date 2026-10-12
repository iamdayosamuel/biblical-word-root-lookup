# Sources and licences

## Strong's Hebrew data (`strongs-hebrew.json`)

- Source: Open Scriptures, github.com/openscriptures/strongs, file `hebrew/strongs-hebrew-dictionary.js`, converted to plain JSON without changing entries.
- Text: James Strong, A Concise Dictionary of the Words in the Hebrew Bible with their Renderings in the King James Version, 1894 (public domain).
- JSON version: Copyright 2010 Open Scriptures, licensed CC-BY-SA, derived from XML. XML e-text from David Instone-Brewer (2LetterLookup.com), with editing, corrections and Unicode transliterations by David Troidl.
- Because of CC-BY-SA, keep this attribution with the file and share any changes to it under the same licence.

## Greek Strong's data (`strongs-greek.json`)

- Source: Open Scriptures, github.com/openscriptures/strongs, file `greek/strongs-greek-dictionary.js`, converted to plain JSON (field `translit` renamed `xlit`; text unchanged).
- Text: James Strong, Dictionary of the Greek Testament, in Strong's Exhaustive Concordance, 1890 (public domain).
- JSON version: Copyright 2009 Open Scriptures, CC-BY-SA. XML e-text prepared in 2006 by Ulrik Petersen. Same attribution and share-alike terms as the Hebrew file.

## Strong's to Benner's table (`strongs-to-benner.csv`)

- Source: the Strong's to Benner's Lexicon index in Benner's Lexicon of Biblical Hebrew (Jeff A. Benner), pp. 526 to 558, printed edition.
- Transcribed by Claude from 17 photos of the page spreads (5,949 rows). Only the number pairs are stored. No Benner's entry text is included. The transcription was spot-checked against known entries (for example H1897 to 874, H3581 to 1612, H7225 to 4119), not proofread row by row.
- Column `table_pages` is the page spread in the book where the row appears, for checking.
- Margin marks in the photos (circles, highlights, brackets) were ignored.

## Ancient alphabet table (`ancient-alphabet.md`) and entry guide (`benner-entry-guide.md`)

- Source: Benner's Lexicon of Biblical Hebrew, pp. 4 to 6.
- The book's copyright notice permits copying any part for educational purposes without prior permission. Keep this skill for educational use and credit Jeff A. Benner and the Lexicon when sharing it. This project is not affiliated with or endorsed by Jeff A. Benner or the Ancient Hebrew Research Center.

## Known low-confidence rows

Check these against the book first if a result looks wrong:

- 6485 and 6486 (p. 549): read as 6485 to 3179, 6486 to 3179 and 6486 to 3182. The repeated 6486 and the two 3179 values are the least certain rows.
- 8232 (p. 556): the photo showed the pair twice with the same value. Stored once as 8232 to 4477.
- Photo rows on the curved inner edge of a page (the left column of right-hand pages and the right column of left-hand pages) are the most likely to carry a misread digit.

When a user confirms or corrects a row, edit the CSV and remove it from this list.

## Not bundled

- Greek to Hebrew (Septuagint) word alignment. Candidate sources: STEP Bible data (github.com/STEPBible/STEPBible-Data, CC BY 4.0, Septuagint file TAGOT still in progress at last check) and the CATSS parallel aligned text (licence unchecked).
- Verse to Strong's mapping. Use an online interlinear (biblehub.com) for that step.
- Benner's entry text. Not included. Users read it in their own copy of the book.
