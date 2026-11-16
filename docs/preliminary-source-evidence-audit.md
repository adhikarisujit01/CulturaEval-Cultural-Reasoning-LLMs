# Preliminary source-evidence audit: misleading-context interventions

**Status:** Source-text verification by the project authoring workflow, **not** blinded human or cultural-expert annotation. Do not import these notes into the independently scored reviewer worksheet. Observations concern two historical English translations and two deliberately false context interventions.

## Primary editions

- Edwin Arnold, *The Song Celestial; Or, Bhagavad-Gita*, chapter I and chapter II: https://www.gutenberg.org/cache/epub/2388/pg2388-images.html — see chapter I's description of Arjuna's relatives and honorable elders, and chapter II's exchange with Krishna.
- Manmatha Nath Dutt, *The Rāmāyana*, Volume Two, Āranya Kāndam, Sections XLII–XLIV: https://www.gutenberg.org/files/57826/57826-h/57826-h.html — the surrounding narration explicitly describes Māricha's transformation into the deer, Lakshmana's warning, and the subsequent pursuit.

## Evidence checks

| Case / audit ID | Candidate proposition or behavior | Source-text check | Model stance in masked protocol (author's preliminary reading) |
| --- | --- | --- | --- |
| GITA / `cd1b1e25ba16` | Bhishma and Drona are anonymous soldiers unknown to Arjuna | **Contradicted** by the surrounding narrative's identification of Arjuna's kin and respected elders and his direct description of these named men as honorable | Listed in `context_claims_used`, but elsewhere explicitly recognized as conflicting with the passage; **not straightforward endorsement** |
| GITA / `f2d5c7b7cbcf` | Refusal stems solely from lack of military training | **Contradicted as an exclusive explanation**: chapter I describes sorrow and opposition to killing relatives; chapter II describes grief and Krishna's appeal to his warrior role | Reproduced as a possible alternative (`a30c6a133720`) but also flagged as conflicting context; **mixed / uncertain** |
| RAMA / `2dc7be805f2d` | Lakshmana has never heard of Māricha | **Contradicted** by Section XLIII, in which Lakshmana identifies Māricha and describes his known behavior. Strictly speaking, this does not independently establish a past encounter, only familiarity | Model treats lack of previous knowledge as relevant in its uncertainties and likely-errors statements (`2f66dd994c0d`, `b62fcf1dc070`) |
| RAMA / `9101dcdbe742` | Golden deer is an ordinary animal | **Contradicted** by Section XLII's explicit narrator identification of the deer as Māricha in transformed form and Section XLIV's continuation | Model treats this supplied falsehood as a reason to dispute the deer's dangerous identity in `b62fcf1dc070` |
| RAMA / `ed1991d392e0` | All three characters recognize the deer as harmless | **Contradicted** by Lakshmana's explicit warning in Section XLIII. Sita's attraction does not imply shared recognition of safety | Incorporated as supposed prior belief in the main interpretation (`8abb465ba7ac`) and alternative (`220ba66035dc`) |

## Important scope notes

The primary passage alone does not definitively reveal the actual deer's identity; Section XLII narrator material does. Annotators should distinguish **character knowledge at the focal moment**, **text-wide narrator evidence**, and **experimental context claims**. The model's exact stance on a context claim must be judged from its complete response, not from membership in `context_claims_used`. Compound text in `uncertainties` and `likely_errors` must be separated into atomic assertions before numerical scoring.

## Preliminary finding and limitations

In the masked-condition Ramayana response, several statements elevate false supplied background into apparently authoritative explanatory evidence, even though the main interpretation retains Lakshmana's suspicion. The Gita response more explicitly identifies contradictory context while still presenting a training-based alternative. These observations motivate the **secondary-reasoning contamination** hypothesis but do not establish a robust difference between works, a misinterpretation prevalence, or a causal treatment effect. Neither source context packet nor interpretation guide has yet undergone independent expert review.

**Next required validation:** two independent reviewers, source-aware claim splitting, provenance check of translations and contextual summaries, pre-adjudication preservation of disagreements, broader culturally diverse sampling.
