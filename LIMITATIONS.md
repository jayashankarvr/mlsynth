# Limitations

mlinflect never emits a form it has not verified; when it cannot, it raises
`NotImplementedError` / `UnsupportedRoot` / `UnsupportedVerb`. The items below are genuine
constraints: distinctions the orthography does not carry, and problems outside this
package's scope. Planned-but-unbuilt features (postpositions, stylistic variants, verb
aspects/participles/voice/causatives) are tracked as future work in the README, not here.

## Distinctions the input does not carry

- **Animacy is not recoverable from spelling.** `a_stem` and chillu plurals therefore
  require an explicit `animacy` and raise without it, since `-മാർ` (human) versus `-കൾ`
  (inanimate) is not predictable from the stem. For the same reason the accusative
  defaults to the overt form; the zero-marked inanimate accusative needs
  `animacy=INANIMATE`.
- **`u_vowel` and `a_stem` match broadly.** A malformed lemma (a samvruthokaram half-u
  written as a bare `-ു` instead of `-്`, or truncated text) is inflected rather than
  rejected, so callers must pass well-formed lemmas.

## Verbs: finite forms only

- `synthesize_verb` covers the finite forms (present, future, past, negation, imperative,
  conditional, hortative, promissive) from the `-ഉക` infinitive. Past allomorphy is selected
  by ending plus an irregular lexicon. The past is partly lexical (native review): the
  irregular lexicon is not exhaustive, so a verb that hits none of the ending-rules takes the
  default `-ഇ`, which is wrong for an unlisted irregular (`നടക്കുക` yields `നടക്കി`, really
  `നടന്നു`). Such default-guess pasts carry `verified=False`, as do imperatives of lexicon
  verbs (which may be suppletive, `വരുക` -> `വാ`, not `വര്`); only confident forms are
  `verified=True`. Non-`-ഉക` infinitives outside the lexicon raise.
- Analytic ability/obligation (`ഓടാൻ പറ്റും`, `ഓടാൻ വേണം`) and aspect/participle/voice
  constructions are not generated.

## Out of scope

- **Noun compounding and external sandhi**: joining two lemmas (e.g. ആന + കുട്ടി ->
  ആനക്കുട്ടി, with gemination) is a separate problem from single-lemma inflection.
