# Authentic source candidate register — initial evidence triage

**Status:** Source discovery only. Not gold annotations, not model evaluations. Add exact excerpt/verse verification and translation-rights checks before dataset inclusion.

| ID | Work / passage candidate | Version and citation | Research challenge | Verification status |
|---|---|---|---|---|
| SRC-001 | *Mahabharata*, Vana Parva: Yaksha's questions and Yudhishthira choosing Nakula | Original episode; a modern prose retelling at https://pressbooks.pub/mahabharata/chapter/the-pandavas-in-exile/ (sections 103–105); historical English poetic rendering: https://sacred.plzhalp.us/hin/ii.htm | Duty, impartiality, family ties and multiple ethical accounts of the choice | Episode confirmed across online renderings; exact primary translation excerpt, rights and verse identifiers still to be verified |
| SRC-002 | *Bhagavad Gita*, Chapter 2: Arjuna asks how he can fight Bhishma and Drona | Edwin Arnold (1885), *The Song Celestial*, https://www.gutenberg.org/ebooks/2388 ; corroborating online chapter at https://www.ancienttexts.org/library/indian/gita/book2.html | Competing obligations, grief, duty and philosophical disagreement | Historical translation identified; exact selected excerpt and verse mapping still to be checked |
| SRC-003 | *Ramayana*, Aranya Kanda, section XLIII: Sita and the golden deer, Lakshmana's suspicion | Historic English text at https://www.gutenberg.org/files/57826/57826-h/57826-h.html | Appearance, deception, situated knowledge, and justified competing interpretations | Section located; translator / edition metadata and exact excerpt still to be verified |

## Rules for admission to the benchmark

1. Confirm exact edition, translator, publication year, section/verse and reuse rights.
2. Store verbatim text with citation and a stable unique excerpt identifier; never silently alter an excerpt.
3. Write a source-supported cultural/contextual evidence packet with links to relevant verses or scholarly commentary.
4. Create a partial packet that is accurate but incomplete; create a misleading packet that is clearly marked as deliberately false in the **private evaluation manifest**, never as authentic tradition.
5. Distinguish evidence-backed interpretations from tentative reviewer hypotheses.
6. Request independent review of both rubric axes; record disagreement.
7. Only then mark examples as ready for LLM evaluation.

## Risks and rationale

A retelling is not automatically the critical Sanskrit edition; it cannot be treated as proof of exact original wording. English translations may differ in philosophically consequential ways. Public-domain status in the United States is not a worldwide copyright conclusion. Reusing numerous excerpts requires separate checks.

This register exists so that progress is reproducible and no unverified episode is passed off as a validated benchmark item.
